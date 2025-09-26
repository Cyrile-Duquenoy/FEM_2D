import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "core"))

import unittest
from geometry.node import Node

class TestNode(unittest.TestCase):
    
    def setUp(self):
        Node.reset_registry()

    def test_creation_node_2d(self):
        n = Node(1.0, 2.0, ids=10)
        self.assertEqual(n.get_coord(), (1.0, 2.0))
        self.assertEqual(n.get_ids(), 10)

    def test_duplicate_node(self):
        Node(1.0, 2.0)
        with self.assertRaises(ValueError):
            Node(1.0, 2.0)

    def test_registry_reset(self):
        Node(1.0, 2.0)
        self.assertEqual(len(Node.all_nodes()), 1)
        Node.reset_registry()
        self.assertEqual(len(Node.all_nodes()), 0)

    def test_set_ids(self):
        n = Node(1.0, 2.0)
        n.set_ids(99)
        self.assertEqual(n.get_ids(), 99)

    def test_str(self):
        n = Node(0.0, 0.0, ids=1)
        self.assertEqual(str(n), "Node(id=1, coord=(0.0, 0.0))")

if __name__ == '__main__':
    unittest.main()






