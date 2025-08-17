import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "core"))

import unittest
from geometry.node import Node
from geometry.element import Element

class TestElement(unittest.TestCase):
    
    def setUp(self):
        Node.reset_registry()

    def test_creation_element_2d(self):
        n1 = Node(0, 0, ids=1)
        n2 = Node(1, 0, ids=2)
        n3 = Node(1, 1, ids=3)
        element = Element([n1, n2, n3], ids=101)
        
        self.assertEqual(element.get_nodes(), [n1, n2, n3])
        self.assertEqual(element.get_ids(), 101)

    def test_element_str(self):
        n1 = Node(0, 0, ids=1)
        n2 = Node(1, 0, ids=2)
        element = Element([n1, n2], ids=200)
        expected_str = "Element(ID=200, Nodes=[1, 2])"
        self.assertEqual(str(element), expected_str)


if __name__ == '__main__':
    unittest.main()
