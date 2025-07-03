from core.node import Node
from core.triangle import Triangle
from core.mesh import Mesh
from visualisation.plot_utils import plot_mesh
from core.elements.p1_element import P1Element

import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    
    n1 = Node(0, 0, ids=1)
    n2 = Node(0, 1, ids=2)
    n3 = Node(1, 0, ids=3)
    n4 = Node(1, 1, ids=4)

    t1 = Triangle(n1, n2, n3, ids=1)
    t2 = Triangle(n2, n3, n4, ids=2)

    mesh = Mesh()
    for node in [n1, n2, n3, n4]:
        mesh.add_node(node)
    for tri in [t1, t2]:
        mesh.add_element(tri)
        
    nodes = mesh.get_nodes()
    elements = mesh.get_elements()

    # Détection des segments de bord
    boundary_segments = mesh.get_boundary_segments()

    # Visualisation
    plot_mesh(mesh)

    # Debug info
    print("Segments de bord :")
    for seg in boundary_segments:
        ids = [n.get_ids() for n in seg.get_nodes()]
        print(f"Segment entre noeuds {ids}")

    print("\nMatrice de connectivité :")
    for conn in mesh.get_connectivity_matrix():
        print(conn)

    print("\nVoisinages des triangles :")
    neighbours = mesh.find_neighbours()
    for tri_id, voisine_ids in neighbours.items():
        print(f"Triangle {tri_id} a pour voisins : {voisine_ids}")

    # Assemblage FEM : matrice de raideur
    n_nodes = len(mesh.get_nodes())
    K_global = np.zeros((n_nodes, n_nodes))
    F_global = np.zeros(n_nodes)

    for triangle in mesh.get_elements():
        element = P1Element(triangle)
        K_local = element.stiffness_matrix()
        indices = [node.get_ids() - 1 for node in triangle._nodes]
        area = element.area
        F_local = np.ones(3) * area / 3 # f=1 constante
        

        for i_local, i_global in enumerate(indices):
            for j_local, j_global in enumerate(indices):
                K_global[i_global, j_global] += K_local[i_local, j_local]

        # Assemblage second membre
        for i_local, i_global in enumerate(indices):
            F_global[i_global] += F_local[i_local]

    print("\nMatrice de raideur globale :")
    print(K_global)
    print("\nSecond membre global :")
    print(F_global)


    dirichlet_nodes = [0, 1]  # indices des noeuds où u=0
    for idx in dirichlet_nodes:
        K_global[idx, :] = 0
        K_global[:, idx] = 0
        K_global[idx, idx] = 1
        F_global[idx] = 0
        
    U = np.linalg.solve(K_global, F_global)
    print("\nSolution nodale U :")
    print(U)
    
    
    # Récupére les coord des noeuds
    x = np.array([node.get_coord()[0] for node in nodes])
    y = np.array([node.get_coord()[1] for node in nodes])
    
    # Récupére connectivité triangles (indices des noeuds)
    triangles = np.array([[node.get_ids()-1 for node in tri._nodes] for tri in elements])
    
    plt.figure(figsize=(6,5))
    
    # Plot solution nodale avec interpolation sur triangles
    plt.tricontourf(x, y, triangles, U, cmap='viridis')
    plt.colorbar(label='Solution U')
    plt.title("Solution FEM (P1) sur le maillage")
    plt.gca().set_aspect('equal')
    plt.show()




