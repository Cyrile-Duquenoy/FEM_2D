import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri


from ..geometry.mesh import Mesh

from .field import Field

class ScalarField(Field):
    def __init__(self, mesh: Mesh, data=None):
        super().__init__(mesh, data)
        self._mesh = mesh
    
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
            triangles = np.array([[node.get_ids() - 1 for node in element._nodes] for element in self._mesh.get_elements()])
            triangulation = tri.Triangulation(x, y, triangles)
            contour = plt.tricontourf(triangulation, c, levels=20, cmap=cmap)
            plt.colorbar(contour, label='Valeur du champ scalaire')
        
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Champ scalaire sur le maillage')
        
        if show:
            plt.show()
            
            

        

    

    
