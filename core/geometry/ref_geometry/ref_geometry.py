import numpy as np


class RefNode:
    def __init__(self, x: float, y: float, ids: int):
        if isinstance(x, float) and isinstance(y, float):
            self._x = x
            self._y = y
            self._coord = (x, y)
        else:
            raise TypeError("Les coordonnées d'un RefNode doivent être de type float")     
        if isinstance(ids, int):
            self._ids = ids
        else:
            raise TypeError("L'indexation des RefNodes doit se faire par des int")

    def __str__(self):
        return f"RefNode(ids={self._ids}, coord={self._coord})"

    def __repr__(self):
        return self.__str__()


class RefTriangle:
    def __init__(self):
        n0 = RefNode(0.0, 0.0, ids=1)
        n1 = RefNode(1.0, 0.0, ids=2)
        n2 = RefNode(0.0, 1.0, ids=3)
        self._ref_triangle = (n0, n1, n2)

        self._grad_ref = np.array([
            [-1, -1],
            [0, 1],
            [1, 0]
        ])

        self._area = 0.5

    def get_area(self):
        return self._area

    def get_grad_ref(self):
        return self._grad_ref

    def get_grad_ref_at_node(self, ids: int):
        if isinstance(ids, int) and ids in range(3):
            return self._grad_ref()[ids]
        else:
            raise ValueError("L'indice doit être un int valant 0, 1 ou 2.")

    def __str__(self):
        return f"RefTrianlge({self._ref_triangle})"

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    n0 = RefNode(0.0, 0.0, ids=1)
    n1 = RefNode(1.0, 0.0, ids=2)
    n2 = RefNode(1.0, 0.0, ids=3)

    T = RefTriangle()
    print(T)
