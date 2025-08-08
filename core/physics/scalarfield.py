import numpy as np
import matplotlib.pyplot as plt



from ..geometry.mesh import Mesh

import matplotlib.tri as tri

class ScalarField:
    def __init__(self, mesh: Mesh, data=None):
        self._mesh = mesh
        nb_nodes = len(mesh.get_nodes())
        
        if data is not None:
            if len(data) != len(mesh.get_nodes()):
                raise ValueError('len(data) doit être égal au nombre de noeuds')
            self._data = data
        else:
            self._data = [0.0] * len(mesh.get_nodes())  # exemple d'initialisation par défaut
    
    
    def plot(self, cmap='viridis', method='surface', show=True):
        nodes = np.array([node.get_coord() for node in self._mesh.get_nodes()])
        x = nodes[:, 0]
        y = nodes[:, 1]
        c = self._data
        
        plt.figure(figsize=(8,6))
        
        if method == 'scatter':
            scatter = plt.scatter(x, y, c=c, cmap=cmap)
            plt.colorbar(scatter, label='Valeur du champ scalaire')
        else:
            import matplotlib.tri as tri
            triangles = np.array([[node.get_ids() - 1 for node in element._nodes] for element in self._mesh.get_elements()])
            print('len triangles', len(triangles))
            triangulation = tri.Triangulation(x, y, triangles)
            contour = plt.tricontourf(triangulation, c, levels=20, cmap=cmap)
            plt.colorbar(contour, label='Valeur du champ scalaire')
        
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Champ scalaire sur le maillage')
        
        if show:
            plt.show()

        

    

    
