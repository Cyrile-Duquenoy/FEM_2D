import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "core"))

import unittest

from geometry.node import Node
from geometry.segment import Segment

class TestSegment(unittest.TestCase):

    def setUp(self):
        Node.reset_registry()

    def test_creation_segment(self):
        n1 = Node(0, 0, ids=1)
        n2 = Node(3, 4, ids=2)
        s = Segment(n1, n2, ids=10, tag="Dirichlet")
        self.assertEqual(s.get_ids(), 10)
        self.assertEqual(s.get_tag(), "Dirichlet")
        self.assertEqual(s.get_nodes(), [n1, n2])

    def test_set_get_tag(self):
        n1 = Node(0, 0)
        n2 = Node(1, 0)
        s = Segment(n1, n2)
        s.set_tag("Neumann")
        self.assertEqual(s.get_tag(), "Neumann")

    def test_length(self):
        n1 = Node(0, 0)
        n2 = Node(3, 4)
        s = Segment(n1, n2)
        self.assertAlmostEqual(s.get_length(), 5.0)

    def test_normal(self):
        n1 = Node(0, 0)
        n2 = Node(1, 0)
        s = Segment(n1, n2)
        nx, ny = s.get_normal()
        # Normale doit être (0,1) ou (0,-1) suivant l'orientation (ici sens direct)
        self.assertAlmostEqual(nx, 0.0)
        self.assertAlmostEqual(ny, 1.0)

    def test_normal_zero_length_segment(self):
        n1 = Node(0, 1)
        n2 = Node(0, 2)
        s = Segment(n1, n2)
        with self.assertRaises(ValueError):
            s.get_normal()

    def test_str(self):
        n1 = Node(0, 0, ids=1)
        n2 = Node(1, 0, ids=2)
        s = Segment(n1, n2, ids=99, tag="Boundary")
        expected_str = "Segment(ID=99, Nodes=[1, 2], Tag='Boundary')"
        self.assertEqual(str(s), expected_str)

if __name__ == '__main__':
    unittest.main()