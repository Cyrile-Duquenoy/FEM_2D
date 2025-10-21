from ..geometry.triangle import Triangle
from ..geometry.ref_geometry import RefTriangle
import numpy as np

_ref_triangle = None


def get_ref_triangle():
    global _ref_triangle
    if _ref_triangle is None:
        _ref_triangle = RefTriangle()
    return _ref_triangle


class P1Element:
    def __init__(self, triangle: Triangle):
        self.triangle = triangle
        self.ref_triangle = get_ref_triangle()
        self.nodes = triangle.get_nodes()
        self.coords = [node.get_coord() for node in self.nodes]
        self.grad_phi, self.area = self.compute_shape_gradients()

        if self.area <= 0:
            print(f"Warning: Triangle with negative/zero area: {self.area}")

    def compute_shape_gradients(self):
        """
        Calcule les gradients des fonctions de forme linéaires (constantes)
        et l'aire du triangle.
        """
        p1, p2, p3 = self.coords[0], self.coords[1], self.coords[2]
        J = np.array([
            [p2[0] - p1[0], p3[0] - p1[0]],
            [p2[1] - p1[1], p3[1] - p1[1]]
        ])

        detJ = np.linalg.det(J)
        area = 0.5 * abs(detJ)

        if abs(detJ) < 1e-12:
            raise ValueError("Triangle dégénéré (aire nulle)")

        invJT = np.linalg.inv(J).T
        grads = self.ref_triangle.get_grad_ref() @ invJT

        return grads, area

    def stiffness_matrix(self):
        """
        Matrice de raideur locale 3x3
        """
        K = np.zeros((3, 3))
        for i in range(3):
            for j in range(3):
                K[i, j] = np.dot(self.grad_phi[i], self.grad_phi[j]) * self.area
        return K

    def mass_matrix(self):
        """
        Matrice de masse locale
        """
        A = self.area
        M = np.full((3, 3), A / 12)
        np.fill_diagonal(M, A / 6)
        return M
