import unittest
from FEM.core.node import Node

class TestNode(unittest.TestCase):
    def test_player_creation(self):
        '''
        caracteristiques = Caracteristiques(PV=100, PM=50)
        player = Player('Elyris', race=Race.HUMAIN, classe=Classe.PALADIN, caracteristiques=caracteristiques)
        self.assertEqual(player._name, 'Elyris')
        self.assertEqual(player._race, Race.HUMAIN)
        self.assertEqual(player.caracteristiques['PV'], 100)
        '''
        node = Node(1,0,2.3, ids = 32)
        self.assertEqual(node._x, 1)

if __name__ == '__main__':
    unittest.main()

