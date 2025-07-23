from .node import Node

class Element:
    def __init__(self, nodes : [Node], ids: int = None):
        self._nodes = nodes
        self.ids = ids
        
    def get_nodes(self):
        return self._nodes
    
    def get_ids(self):
        return self.ids
    
    def get_dimension(self):
        return self._nodes[0].get_dimension()
    
    def __str__(self):
        node_ids = ", ".join(str(n.get_ids()) for n in self._nodes)
        return f"{self.__class__.__name__}(ID={self.ids}, Nodes=[{node_ids}])"
    
