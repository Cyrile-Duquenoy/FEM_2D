from .node import Node
from .element import Element
from .segment import Segment

class Triangle(Element):
    
    _registry = []
    
    def __init__(self, n1: Node, n2: Node, n3: Node, ids: int = 0):
        super().__init__([n1, n2, n3], ids)
        self._faces = [
            (n1, n2),
            (n1, n3),
            (n2, n3)
        ]
        self._local_ident = [
            (1, n1.get_ids()),
            (2, n2.get_ids()),
            (3, n3.get_ids())
        ]
        self._nodes = [n1, n2, n3]
        Triangle._registry.append(self)

    def get_faces(self):
        return self._faces

    def get_local_ident(self):
        return self._local_ident

    def get_area(self):
        #(n1, n2, n3) = (self.n1, self.n2, self.n3)
        x1, y1 = n1.get_coord()
        x2, y2 = n2.get_coord()
        x3, y3 = n3.get_coord()
        return 0.5 * abs((x2 - x1)*(y3 - y1) - (x3 - x1)*(y2 - y1))
    
    @classmethod 
    def all_triangles(cls):
        return cls._registry
    
    @classmethod 
    def reset_registry(cls):
        cls._registry = []
<<<<<<< Updated upstream
=======


        
        
        

    
>>>>>>> Stashed changes


