import numpy as np
import matplotlib.pyplot as plt

class Node:
    
    _registry = {}  # dictionnaire coord -> node
    
    def __init__(self, x: float, y: float, ids: int = None, is_boundary: bool = False):
        self._x = x
        self._y = y
        self.ids = ids
        self._is_boundary = is_boundary
        
        key = self.get_coord()
        
        if key in Node._registry:
            raise ValueError(f"Node at {key} already exists.")
        else:
            Node._registry[key] = self
        
    def set_ids(self, ids: int):
        self.ids = ids
        
    def get_ids(self):
        return self.ids
        
    def get_coord(self):
            return (self._x, self._y)

    @classmethod 
    def all_nodes(cls):
        return list(cls._registry.values())
    
    @classmethod 
    def reset_registry(cls):
        cls._registry = {}
    
    @classmethod
    def get_node(cls, x: float, y: float):
        key = (x, y)
        return cls._registry.get(key, None)
    
    def __str__(self):
        return f'Node(id={self.ids}, coord={self.get_coord()})'
    
    def __repr__(self):
        return f'Node(id={self.ids}, coord={self.get_coord()})'

        
if __name__ == '__main__':
    n1 = Node(0,0)
    n2 = Node(1,0)
    n3 = Node(0,1)
    print(n1,n2,n3)
    

        

