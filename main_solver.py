from core.geometry.node import Node
from core.geometry.triangle import Triangle
from core.geometry.mesh import Mesh
from visualisation.plot_utils import plot_mesh
from core.elements.p1_element import P1Element

import numpy as np
import matplotlib.pyplot as plt

from core.geometry import square_mesh, GEOMETRY_MAPPING, Geometry
from core.solver import FEMSolver

#%% Création Maillage
h = 1.0 # hauteur
l = 1.0 # largeur
n = 25  # nombre de divisions par côté

# Réinitialiser le registre des nœuds pour s'assurer d'un maillage propre
Node.reset_registry()

mesh = Mesh.from_geometry(Geometry.SQUARE, h=h, l=l, n=n)


for i, node in enumerate(mesh.get_nodes()):
    node.set_ids(i) # Re-indexer les IDs de 0 à num_nodes-1

'''
mesh.get_boundary_segments()
'''

#%%
# Coefficient de diffusion
def k_coefficient(x, y):
    return 1.0 # Coefficient constant pour l'exemple

# Terme source
def source_term(x, y):
    # Exemple: f(x,y) = 10
    return 1

#%% Conditions Limites

# Dirichlet
dirichlet_bcs = {}

# Bord gauche (x=0)
for node in mesh.get_nodes():
    x, y = node.get_coord()
    if np.isclose(x, 0.0): # or np.isclose(0.0, y):
        dirichlet_bcs[node.get_ids()] = 0.0
    elif np.isclose(x, 1.0): # or np.isclose(1.0, y):
        dirichlet_bcs[node.get_ids()] = 0.0


# Neumann (flux = 0 sur les bords haut et bas)
neumann_bcs = {}
# Exemple: flux = 5 sur le bord supérieur (y=1)
# for segment in mesh.get_boundary_segments():
#     n1, n2 = segment.get_nodes()
#     x1, y1 = n1.get_coord()
#     x2, y2 = n2.get_coord()
#     if np.isclose(y1, 1.0) and np.isclose(y2, 1.0): # Segment sur le bord supérieur
#         neumann_bcs[segment.get_ids()] = 5.0


#%% Initialiser et exécuter le solveur
solver = FEMSolver(mesh)
solver.assemble_system(k_coefficient=k_coefficient, source_term_func=source_term)
solver.apply_boundary_conditions(dirichlet_bcs=dirichlet_bcs, neumann_bcs=neumann_bcs)
solution = solver.solve()

print("Solution calculée aux nœuds (premières 10 valeurs):")
print(solution[:10])

#%% Post-traitement et visualisation


# Extraire les coordonnées des nœuds et la solution
node_coords = np.array([node.get_coord() for node in mesh.get_nodes()])
x_coords = node_coords[:, 0]
y_coords = node_coords[:, 1]
# Vérifiez que la solution a la bonne forme
if len(solution) != len(node_coords):
    raise ValueError("La longueur de la solution ne correspond pas au nombre de nœuds.")
    

# Visualisation du maillage et de la solution
'''
plt.figure(figsize=(10, 8))
plt.tricontourf(x_coords, y_coords, solution, levels=20, cmap='viridis')
plt.colorbar(label='Solution u')

plt.triplot(x_coords, y_coords, np.array([
    [node.get_ids() for node in el.get_nodes()] for el in mesh.get_elements() if isinstance(el, Triangle)
]), color='k', lw=0.5, alpha=0.5)

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Solution du problème de Poisson 2D')
plt.scatter(x_coords, y_coords, color='red', s=10)
#plt.legend()
plt.grid(False)
plt.show()
'''


# Extraire les coordonnées et la solution
node_coords = np.array([node.get_coord() for node in mesh.get_nodes()])
x = node_coords[:, 0]
y = node_coords[:, 1]
# Créer la figure
plt.figure(figsize=(8, 6))
# Afficher UNIQUEMENT la solution en couleurs
contour = plt.tricontourf(x, y, solution, levels=20, cmap='turbo')
plt.colorbar(contour, label='Valeur de la solution')
# Options esthétiques
plt.title('Distribution de la solution FEM')
plt.xlabel('Axe X')
plt.ylabel('Axe Y')
plt.tight_layout()  # Optimise l'espace
plt.show()



