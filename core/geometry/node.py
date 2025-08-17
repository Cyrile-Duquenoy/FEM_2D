import numpy as np
import matplotlib.pyplot as plt

class Node:
    
    _registry = {}  # dictionnaire coord -> node
    
    def __init__(self, x: float, y: float, z: float = None, ids: int = None):
        self._x = x
        self._y = y
        self._z = z
        self.ids = ids
        
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
        if self._z is None:
            return (self._x, self._y)
        else:
            return (self._x, self._y, self._z)
    
    def get_dimension(self):
        return 2 if self._z is None else 3
        
    @classmethod 
    def all_nodes(cls):
        return list(cls._registry.values())
    
    @classmethod 
    def reset_registry(cls):
        cls._registry = {}
        
    def __str__(self):
        return f'Node(id={self.ids}, coord={self.get_coord()})'
<<<<<<< Updated upstream
=======
    
    def __repr__(self):
        return f'Node(id={self.ids}, coord={self.get_coord()})'
    
    def dist(self, node: 'Node'):
        if len(self.get_coord()) != len(node.get_coord()):
            raise ValueError("Les noeuds doivent être de même dimensions afin de calculer leur distance.")
        res = 0
        for i in range(len(node.get_coord())):
            res += (node.get_coord()[i] - self.get_coord()[i])**2
        return np.sqrt(res)
>>>>>>> Stashed changes

        
if __name__ == '__main__':
    n1 = Node(0,0)
    n2 = Node(1,0)
    n3 = Node(0,1)


        

