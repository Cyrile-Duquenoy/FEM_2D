import numpy as np
import matplotlib.pyplot as plt

class Node:
    def __init__(self, x: float, y: float, z: float = None, ids: int = None):
        self._x = x
        self._y = y
        self._z = z
        self.ids = ids
        
    def set_ids(self, ids:int):
        self.ids = ids
        
    def get_ids(self):
        return self.ids
        
    def get_coord(self):
        if self._z is None:
            return ( self._x, self._y)
        else:
            return ( self._x, self._y,  self._z)
    
    def get_dimension(self):
        if self._z is None:
            return 2 
        else :
            return 3
        
        
    def __str__(self):
        if self._z is None:
            return f'Node(id={self.ids}, coord=({self._x}, {self._y}))'
        else:
            return f'Node(id={self.ids}, coord=({self._x}, {self._y}, {self._z}))'
        
        
if __name__ == '__main__':
    n1 = Node(0,0)
    n2 = Node(1,0)
    n3 = Node(0,1)

        

