from .node import Node

class Element:
    def __init__(self, nodes : [Node], ids: int = None):
        self._nodes = nodes
        self.ids = ids
        
    def get_nodes(self):
        return self._nodes
    
    def get_ids(self):
        return self.ids
    
    def __str__(self):
        node_ids = ", ".join(str(n.get_ids()) for n in self._nodes)
        return f"{self.__class__.__name__}(ID={self.ids}, Nodes=[{node_ids}])"
    
    def get_diameter(self):
        diam = 0
        nodes = self.get_nodes()
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                dist = nodes[i].dist(nodes[j])
                if dist > diam:
                    diam = dist
        return diam
    
    
    def is_convex(self):
        pass

            
    
