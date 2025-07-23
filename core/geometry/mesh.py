from .node import Node
from .element import Element
from .segment import Segment
from .triangle import Triangle


class Mesh:
    def __init__(self, nodes: list = None, elements: list = None, segments: list = None):
        self._nodes = [] if nodes is None else nodes
        self._elements = [] if elements is None else elements
        self._segments = [] if segments is None else segments
        
        
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
        return self._segments
        
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
                # Tri des IDs pour que l’ordre n’ait pas d’importance
                id_pair = tuple(sorted((n1.get_ids(), n2.get_ids())))
                segment_count[id_pair] += 1
                if id_pair not in segment_map:
                    segment_map[id_pair] = (n1, n2)
    
        self._segments = []
        for id_pair, count in segment_count.items():
            if count == 1:
                n1, n2 = segment_map[id_pair]
                self._segments.append(Segment(n1, n2))
    
        return self._segments
    

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
        
