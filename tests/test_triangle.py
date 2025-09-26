import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "core"))

import unittest

from geometry.node import Node
from geometry.element import Element
from geometry.triangle import Triangle

class TestTriangle(unittest.TestCase):
    
    def setUp(self):
        Node.reset_registry()
        Triangle.reset_registry()

    def test_creation_triangle_and_registry(self):
        n1 = Node(0, 0, ids=1)
        n2 = Node(1, 0, ids=2)
        n3 = Node(0, 1, ids=3)
        tri = Triangle(n1, n2, n3, ids=10)
        
        self.assertEqual(tri.get_ids(), 10)
        self.assertEqual(len(Triangle.all_triangles()), 1)
        self.assertIn(tri, Triangle.all_triangles())

    def test_triangle_nodes_ordering(self):
        n1 = Node(1, 1, ids=1)
        n2 = Node(0, 0, ids=2)
        n3 = Node(1, 0, ids=3)
        tri = Triangle(n1, n2, n3)
        nodes_coords = [node.get_coord() for node in tri.get_nodes()]
        
        # Le premier noeud doit être celui avec le plus petit (x,y)
        self.assertEqual(nodes_coords[0], min(nodes_coords))

    def test_get_faces(self):
        n1 = Node(0, 0, ids=1)
        n2 = Node(1, 0, ids=2)
        n3 = Node(0, 1, ids=3)
        tri = Triangle(n1, n2, n3)
        faces = tri.get_faces()
        expected_faces = [(n1, n2), (n1, n3), (n2, n3)]
        self.assertEqual(faces, expected_faces)

    def test_get_local_ident(self):
        n1 = Node(0, 0, ids=1)
        n2 = Node(1, 0, ids=2)
        n3 = Node(0, 1, ids=3)
        tri = Triangle(n1, n2, n3)
        local_ids = tri.get_local_ident()
        expected = [(1, 1), (2, 2), (3, 3)]
        self.assertEqual(local_ids, expected)

    def test_get_area(self):
        n1 = Node(0, 0)
        n2 = Node(1, 0)
        n3 = Node(0, 1)
        tri = Triangle(n1, n2, n3)
        area = tri.get_area()
        self.assertAlmostEqual(area, 0.5)

    def test_aligned_nodes_raise(self):
        n1 = Node(0, 0)
        n2 = Node(1, 1)
        n3 = Node(2, 2)
        with self.assertRaises(ValueError):
            Triangle(n1, n2, n3)

    def test_registry_reset(self):
        n1 = Node(0, 0)
        n2 = Node(1, 0)
        n3 = Node(0, 1)
        tri = Triangle(n1, n2, n3)
        self.assertEqual(len(Triangle.all_triangles()), 1)
        Triangle.reset_registry()
        self.assertEqual(len(Triangle.all_triangles()), 0)


if __name__ == '__main__':
    unittest.main()

