from ..triangle import Triangle
import numpy as np

class P1Element:
    def __init__(self, triangle):
        self.triangle = triangle
        self.nodes = triangle._nodes
        self.coords = np.array([node.get_coord() for node in self.nodes])
        self.grad_phi, self.area = self.compute_shape_gradients()

    def compute_shape_gradients(self):
        """
        Calcule les gradients des fonctions de forme linéaires (constantes)
        et l'aire du triangle.
        """
        p1, p2, p3 = self.coords
        J = np.array([
            [p2[0] - p1[0], p3[0] - p1[0]],
            [p2[1] - p1[1], p3[1] - p1[1]]
        ])
        detJ = np.linalg.det(J)
        area = 0.5 * abs(detJ)

        # Gradients des fonctions de forme de référence (tri unité)
        grad_ref = np.array([
            [-1, -1],
            [1, 0],
            [0, 1]
        ])

        invJT = np.linalg.inv(J).T
        grads = grad_ref @ invJT  # (3,2)

        return grads, area

    def stiffness_matrix(self):
        """
        Matrice de raideur locale 3x3 : K_ij = (grad phi_i . grad phi_j) * area
        """
        K = np.zeros((3, 3))
        for i in range(3):
            for j in range(3):
                K[i, j] = np.dot(self.grad_phi[i], self.grad_phi[j]) * self.area
        return K

    def mass_matrix(self):
        """
        Matrice de masse locale 3x3 (P1):
        M_ij = area / 12 si i != j
        M_ii = area / 6
        """
        A = self.area
        M = np.full((3, 3), A / 12)
        np.fill_diagonal(M, A / 6)
        return M



