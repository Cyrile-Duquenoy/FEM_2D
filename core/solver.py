import numpy as np
from scipy.sparse import lil_matrix, csc_matrix
from scipy.sparse.linalg import spsolve

from .geometry.triangle import Triangle
from .elements.p1_element import P1Element
from .geometry.mesh import Mesh

class FEMSolver:
    def __init__(self, mesh: Mesh):
        self.mesh = mesh
        self.num_nodes = len(self.mesh.get_nodes())
        self.K_global = None  
        self.F_global = None  
        self.U_solution = None 

    def assemble_system(self, k_coefficient=1.0, source_term_func=None):
        self.K_global = lil_matrix((self.num_nodes, self.num_nodes))
        self.F_global = np.zeros(self.num_nodes)
        node_to_global_idx = {node.get_ids(): i for i, node in enumerate(self.mesh.get_nodes())}


        for element in self.mesh.get_elements():
            if isinstance(element, Triangle):
                p1_el = P1Element(element)
                
                # Matrice de rigidité élémentaire (K_e)
                if callable(k_coefficient):
                    # Calculer k au centroïde de l'élément pour une approximation
                    centroid_x = np.mean([n.get_coord()[0] for n in element.get_nodes()])
                    centroid_y = np.mean([n.get_coord()[1] for n in element.get_nodes()])
                    k_val = k_coefficient(centroid_x, centroid_y)
                else:
                    k_val = k_coefficient
                
                Ke = p1_el.stiffness_matrix() * k_val

                Fe = np.zeros(3)
                if source_term_func:
                    # Pour les fonctions de forme P1, l'intégration de f sur l'élément est simplifiée
                    centroid_x = np.mean([n.get_coord()[0] for n in element.get_nodes()])
                    centroid_y = np.mean([n.get_coord()[1] for n in element.get_nodes()])
                    f_val = source_term_func(centroid_x, centroid_y)
                    Fe = np.ones(3) * f_val * p1_el.area / 3.0 # Répartition égale du terme source sur les nœuds

                # Obtenir les indices globaux des nœuds de l'élément
                global_indices = [node_to_global_idx[n.get_ids()] for n in element.get_nodes()]

                # Assemblage
                for local_i, global_i in enumerate(global_indices):
                    for local_j, global_j in enumerate(global_indices):
                        self.K_global[global_i, global_j] += Ke[local_i, local_j]
                    self.F_global[global_i] += Fe[local_i]

        self.K_global = self.K_global.tocsc() # Convertir en format CSC pour la résolution
        
    
    def apply_boundary_conditions(self, dirichlet_bcs: dict = None, neumann_bcs: dict = None):
        if dirichlet_bcs is None:
            dirichlet_bcs = {}
        if neumann_bcs is None:
            neumann_bcs = {}
    
        # Mapping des IDs vers les indices globaux
        node_to_global_idx = {node.get_ids(): i for i, node in enumerate(self.mesh.get_nodes())}
    
        # Neumann
        boundary_segments = self.mesh.get_boundary_segments()
        segment_map = {s.get_ids(): s for s in boundary_segments}
    
        for segment_id, flux_value in neumann_bcs.items():
            segment = segment_map.get(segment_id)
            if segment:
                length = segment.get_length()
                n1, n2 = segment.get_nodes()
                global_idx_n1 = node_to_global_idx[n1.get_ids()]
                global_idx_n2 = node_to_global_idx[n2.get_ids()]
    
                # Distribution du flux sur les nœuds (quadrature linéaire)
                self.F_global[global_idx_n1] += flux_value * length / 2.0
                self.F_global[global_idx_n2] += flux_value * length / 2.0
    
        # Dirichlet
        self.K_global = self.K_global.tolil()
    
        for node_id, prescribed_value in dirichlet_bcs.items():
            global_idx = node_to_global_idx.get(node_id)
            if global_idx is not None:
                # Soustraire la contribution aux autres équations
                for k in range(self.num_nodes):
                    if k != global_idx:
                        self.F_global[k] -= self.K_global[k, global_idx] * prescribed_value
                        # Mettre à zéro la colonne (symétrisation)
                        self.K_global[k, global_idx] = 0
    
                # Modifier la ligne du nœud de Dirichlet
                self.K_global[global_idx, :] = 0
                self.K_global[global_idx, global_idx] = 1.0
                self.F_global[global_idx] = prescribed_value
            else:
                print(f"Warning: Dirichlet BC for non-existent node ID {node_id}")
    
        self.K_global = self.K_global.tocsc()
    
    def solve(self):
        if self.K_global is None or self.F_global is None:
            raise ValueError("Les matrices globales n'ont pas été assemblées. Appelez assemble_system() d'abord.")
        
        # Résoud le système linéaire
        self.U_solution = spsolve(self.K_global, self.F_global)
        return self.U_solution

    def get_solution_at_node(self, node_id):
        if self.U_solution is None:
            raise ValueError("Le problème n'a pas encore été résolu.")
        
        # Re-indexer les nœuds pour s'assurer que les IDs sont des indices valides
        node_to_global_idx = {node.get_ids(): i for i, node in enumerate(self.mesh.get_nodes())}
        global_idx = node_to_global_idx.get(node_id)

        if global_idx is not None:
            return self.U_solution[global_idx]
        else:
            raise ValueError(f"Node with ID {node_id} not found in the mesh.")




