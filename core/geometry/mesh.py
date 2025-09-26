from .node import Node
from .element import Element
from .segment import Segment
from .triangle import Triangle
from .element import Element

import numpy as np

import numpy as np
import networkx as nx

class Mesh:
    def __init__(self, nodes: list[Node] = None, elements: list[Element] = None, segments: list[Segment] = None):
        self._nodes = [] if nodes is None else nodes
        self._elements = [] if elements is None else elements
        self._segments = self.set_all_segments() if segments is None else segments
        
        
    def add_node(self, node: Node):
        self._nodes.append(node)
        
    def add_element(self, elmt: Element):
        self._elements.append(elmt)
        
    def add_segment(self, segment: Segment):
        self._segments.append(segment)
    
    def get_nodes(self):
        return self._nodes
    
    def get_elements(self):
        return self._elements
    
    def get_segments(self):
        N = [seg for seg in self._segments]
        return N
    
    def set_all_segments(self):
        seen_edges = {}
        
        for element in self._elements:
            nodes = element.get_nodes()
            num_nodes = len(nodes)
            
            for i in range(num_nodes):
                n1 = nodes[i]
                n2 = nodes[(i + 1) % num_nodes]  # suivant, en bouclant
                edge_key = tuple(sorted((n1.get_ids(), n2.get_ids())))
                
                if edge_key not in seen_edges:
                    seen_edges[edge_key] = (n1, n2)
        
        return [Segment(n1, n2) for n1, n2 in seen_edges.values()]

    def get_boundary_segments(self):
        from collections import defaultdict
        
        segment_count = defaultdict(int)
        segment_map = {}

        N = [seg for seg in self._segments]
        return N
    
    def set_all_segments(self):
        from collections import defaultdict
    
        segment_count = defaultdict(int)   # Compte combien de fois chaque arête est vue
        segment_map = {}                   # Associe chaque arête à ses deux noeuds
    
        for element in self._elements:
            if not isinstance(element, Triangle):
                continue
    
            nodes = element.get_nodes()
    
            # Crée les 3 arêtes d'un triangle
            edges = [
                (nodes[0], nodes[1]),
                (nodes[1], nodes[2]),
                (nodes[2], nodes[0])
            ]
    
            for n1, n2 in edges:
                # Clé d'arête : paire d'IDs ordonnée (ordre n'a pas d'importance)
                edge_key = tuple(sorted((n1.get_ids(), n2.get_ids())))
                segment_count[edge_key] += 1
                if edge_key not in segment_map:
                    segment_map[edge_key] = (n1, n2)
    
        # Création des segments
        segments = []
        for i, (edge_key, (n1, n2)) in enumerate(segment_map.items()):
            is_boundary = segment_count[edge_key] == 1
            seg = Segment(n1, n2, ids=i + 1, boundary = is_boundary)
            segments.append(seg)
            self._segment = segments
        return segments

    
    def get_boundary_segments(self):
        return [s for s in self.get_segments() if s.is_boundary()]

    def get_connectivity_matrix(self):
        connectivity = []
        for elmt in self._elements:
            node_ids = [node.get_ids() for node in elmt.get_nodes()]
            connectivity.append(node_ids)
        return connectivity
    
    
    def find_neighbours(self):
        from collections import defaultdict
    
        edge_to_triangle = defaultdict(list)
    
        for i, elmt in enumerate(self._elements):
            if not isinstance(elmt, Triangle):
                continue
            nodes = elmt.get_nodes()
            edges = [
                tuple(sorted((nodes[0].get_ids(), nodes[1].get_ids()))),
                tuple(sorted((nodes[1].get_ids(), nodes[2].get_ids()))),
                tuple(sorted((nodes[2].get_ids(), nodes[0].get_ids())))
            ]
            for edge in edges:
                edge_to_triangle[edge].append(i)
    
        neighbours = defaultdict(set)
    
        for edge, triangles in edge_to_triangle.items():
            if len(triangles) == 2:
                t1, t2 = triangles
                neighbours[t1].add(t2)
                neighbours[t2].add(t1)
    
        return {k: list(v) for k, v in neighbours.items()}
    

    def assign_connected_aligned_tags(self):
        boundary_segments = self.get_boundary_segments()
        G = nx.Graph()
    
        # Ajouter chaque segment comme noeud dans le graphe (avec son id)
        for i, seg in enumerate(boundary_segments):
            G.add_node(i)
    
        def are_aligned(seg1, seg2, tol=1e-12):
            # Vérifie si 2 segments sont alignés (colinéaires)
            n1a, n1b = seg1.get_nodes()
            n2a, n2b = seg2.get_nodes()
    
            def vector(p1, p2):
                return p2[0]-p1[0], p2[1]-p1[1]
    
            # Vecteurs des 2 segments
            v1 = vector(n1a.get_coord(), n1b.get_coord())
            v2 = vector(n2a.get_coord(), n2b.get_coord())
    
            # Produit vectoriel = 0 si colinéaires
            cross = v1[0]*v2[1] - v1[1]*v2[0]
            return abs(cross) < tol
    
        # Créer les arêtes selon les critères
        for i, seg_i in enumerate(boundary_segments):
            for j, seg_j in enumerate(boundary_segments):
                if i >= j:
                    continue
                # Vérifier connexion : partagent un noeud ?
                nodes_i = {n.get_ids() for n in seg_i.get_nodes()}
                nodes_j = {n.get_ids() for n in seg_j.get_nodes()}
                if nodes_i.intersection(nodes_j):
                    # Vérifier alignement
                    if are_aligned(seg_i, seg_j):
                        G.add_edge(i, j)
    
        # Trouver les composantes connexes
        connected_components = list(nx.connected_components(G))
    
        # Assignation des tags
        for tag_id, component in enumerate(connected_components, start=1):
            for seg_idx in component:
                boundary_segments[seg_idx].set_tag(f"boundary_{tag_id}")
    
        return boundary_segments

    
    @staticmethod
    def from_geometry(geometry, **kwargs):
        from .geometry import Geometry, GEOMETRY_MAPPING
        if geometry not in GEOMETRY_MAPPING:
            raise ValueError(f"Géométrie non supportée : {geometry}")
        mesh_func = GEOMETRY_MAPPING[geometry]
        return mesh_func(**kwargs)
        
