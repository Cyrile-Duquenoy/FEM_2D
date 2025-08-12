from enum import Enum
from .node import Node
from .triangle import Triangle
from .mesh import Mesh
from .segment import Segment

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
    segments = []

    dx = l / n
    dy = h / n
    
    # Création des Nodes
    for j in range(n+1):
        for i in range(n+1):
            node_id = j * (n+1) + i + 1
            is_boundary = (i == 0 or i == n or j == 0 or j == n)
            node = Node(i*dx, j*dy, ids=node_id, is_boundary=is_boundary)
            nodes.append(node)
            
    # Création des Triangles
    for j in range(n):
        for i in range(n):
            n1 = j * (n+1) + i
            n2 = n1 + 1
            n3 = n1 + (n+1)
            n4 = n3 + 1
            elements.append(Triangle(nodes[n1], nodes[n2], nodes[n4]))
            elements.append(Triangle(nodes[n1], nodes[n4], nodes[n3]))
       
    mesh = Mesh(nodes, elements)

    return mesh


GEOMETRY_MAPPING = {
    Geometry.SQUARE: square_mesh,
    }

