from enum import Enum
from .node import Node
from .triangle import Triangle
from .mesh import Mesh

class Geometry(Enum):
    SQUARE = 'SQUARE'
    RECTANGLE = 'RECTANGLE'
    CIRCLE = 'CIRCLE'
    
    def __str__(self):
        return self.value

class Square:
    def __init__(self, h: float, l: float, n: int):
        self._mesh = square_mesh(h, l, n)

def square_mesh(h: float, l: float, n: int):
    nodes = []
    elements = []
    dx = l / n
    dy = h / n
    
    for j in range(n+1):
        for i in range(n+1):
            '''
            node = Node(i * dx, j * dy, ids=i+j+1)
            nodes.append(node)
            '''
            node_id = j * (n+1) + i + 1
            node = Node(i*dx, j*dy, ids=node_id)
            nodes.append(node)
            
    for j in range(n):
        for i in range(n):
            n1 = j * (n+1) + i
            n2 = n1 + 1
            n3 = n1 + (n+1)
            n4 = n3 + 1
            elements.append(Triangle(nodes[n1], nodes[n2], nodes[n4]))
            elements.append(Triangle(nodes[n1], nodes[n4], nodes[n3]))
<<<<<<< Updated upstream

    mesh = Mesh()
    for node in nodes:
        mesh.add_node(node)
    for elmt in elements:
        mesh.add_element(elmt)
=======
       
    mesh = Mesh(nodes, elements)
    mesh.assign_connected_aligned_tags()
    
>>>>>>> Stashed changes
    return mesh


    
GEOMETRY_MAPPING = {
    Geometry.SQUARE: square_mesh,
    }

