from .node import Node
from .element import Element
from .segment import Segment
from .triangle import Triangle
from .element import Element

import numpy as np

class Mesh:
    def __init__(self, nodes: list[Node] = None, elements: list[Element] = None):
        self._nodes = [] if nodes is None else nodes
        self._elements = [] if elements is None else elements
        self._segments = self.set_all_segments()
        
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
        
        for element in self._elements:
            if not isinstance(element, Triangle):
                continue
            
            nodes = element.get_nodes()
            edges = [
                (nodes[0], nodes[1]),
                (nodes[1], nodes[2]),
                (nodes[2], nodes[0])
            ]
            
            for n1, n2 in edges:
                id_pair = tuple(sorted((n1.get_ids(), n2.get_ids())))
                segment_count[id_pair] += 1
                if id_pair not in segment_map:
                    segment_map[id_pair] = (n1, n2)
        
        boundary_segments = []
        for id_pair, count in segment_count.items():
            if count == 1:
                n1, n2 = segment_map[id_pair]
                
                # Chercher un segment déjà existant avec ces deux nodes
                existing = next(
                    (seg for seg in self._segments 
                     if {n.get_ids() for n in seg.get_nodes()} == {n1.get_ids(), n2.get_ids()}),
                    None
                )
                
                if existing:
                    segment = existing
                else:
                    segment = Segment(n1, n2)
                
                segment._boundary = True
                
                boundary_segments.append(segment)
        
        return boundary_segments

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
    
    @staticmethod
    def from_geometry(geometry, **kwargs):
        from .geometry import Geometry, GEOMETRY_MAPPING
        if geometry not in GEOMETRY_MAPPING:
            raise ValueError(f"Géométrie non supportée : {geometry}")
        mesh_func = GEOMETRY_MAPPING[geometry]
        return mesh_func(**kwargs)
        
