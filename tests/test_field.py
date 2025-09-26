import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "core"))

import unittest
from physics.field import Field


class MockMesh:
    """Mock minimaliste de Mesh avec juste un attribut nodes."""
    def __init__(self, nodes):
        self.nodes = nodes


class TestField(unittest.TestCase):

    def setUp(self):
        # Création d'un maillage fictif avec 3 noeuds 2D
        nodes = np.array([[0, 0], [1, 0], [0, 1]])
        self.mesh = MockMesh(nodes)
        self.field = Field(self.mesh)

    def test_initialisation(self):
        # Vérifier que les champs sont bien initialisés à zéro
        np.testing.assert_array_equal(self.field.stress, np.zeros((3,2,2)))
        np.testing.assert_array_equal(self.field.strain, np.zeros((3,2,2)))

    def test_set_get_contrainte(self):
        c = np.array([[10, 1], [1, 5]])
        self.field.set_stress(1, c)
        np.testing.assert_array_equal(self.field.get_stress(1), c)

    def test_set_get_deformation(self):
        d = np.array([[0.01, 0.001], [0.001, 0.005]])
        self.field.set_strain(2, d)
        np.testing.assert_array_equal(self.field.get_strain(2), d)

    def test_plot_field_norm(self):
        # On met des valeurs non-nulles pour tester le plot (pas d'assertion)
        c0 = np.array([[1, 0], [0, 1]])
        self.field.set_stress(0, c0)
        # Juste vérifier que la méthode s'appelle sans erreur
        try:
            self.field.plot_field_norm('stress')
        except Exception as e:
            self.fail(f"plot_field_norm a levé une exception: {e}")

        with self.assertRaises(ValueError):
            self.field.plot_field_norm('invalid_field')


if __name__ == "__main__":
    unittest.main()
