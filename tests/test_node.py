import unittest
from FEM.core.node import Node

class TestNode(unittest.TestCase):
    def test_player_creation(self):
        node = Node(1,0,2.3, ids = 32)
        self.assertEqual(node._x, 1)

if __name__ == '__main__':
    unittest.main()

