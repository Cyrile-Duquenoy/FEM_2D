from .node import Node
from .element import Element


class Segment(Element):
    def __init__(self, n1: Node,
                 n2: Node,
                 ids: int = 0,
                 tag: str = "",
                 boundary=False):
        super().__init__([n1, n2], ids)
        self._tag = tag  # Tag la condition associée (Dirichlet, Neumann, etc.)
        self._boundary = boundary
        self._ids = ids

    def __str__(self):
        ids = [n.get_ids() for n in self._nodes]
        return f"Segment(ID={self._ids}, Nodes={ids}, Tag={self._tag}, boundary = {self._boundary}')"

    def __repr__(self):
        return self.__str__()

    def get_tag(self):
        return self._tag

    def set_tag(self, tag: str):
        self._tag = tag

    def get_length(self):
        n1, n2 = self._nodes
        x1, y1 = n1.get_coord()
        x2, y2 = n2.get_coord()
        return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

    def get_normal(self):
        n1, n2 = self._nodes
        x1, y1 = n1.get_coord()
        x2, y2 = n2.get_coord()

        dx = x2 - x1
        dy = y2 - y1

        # Normale tournée vers la gauche (sens direct en 2D)
        nx = -dy
        ny = dx

        norm = (nx**2 + ny**2)**0.5
        if norm == 0:
            raise ValueError("Segment de longueur nulle, normale indéfinie.")

        return (nx / norm, ny / norm)

    def is_boundary(self):
        return self._boundary
