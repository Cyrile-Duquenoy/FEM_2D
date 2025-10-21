from core.geometry.node import Node
from core.geometry.mesh import Mesh
from visualisation.plot_utils import plot_mesh

import numpy as np

from core.geometry import Geometry
from core.solver import FEMSolver

from core.physics.scalarfield import ScalarField

# %% Création Maillage
h = 1.0  # hauteur
l = 1.0  # largeur
n = 4  # nombre de divisions par côté

# Réinitialiser le registre des nœuds pour s'assurer d'un maillage propre
Node.reset_registry()

mesh = Mesh.from_geometry(Geometry.SQUARE, h=h, l=l, n=n)

# %%
# Coefficient de diffusion


def k_coefficient(x, y):
    return 1


# Terme source
def source_term(x, y):
    # Exemple: f(x,y) = 1
    # return 1
    return 2 * np.pi**2 * np.sin(np.pi * x) * np.sin(np.pi * y)


# %% Conditions Limites

'''
dirichlet_value = 0
dirichlet_bcs = {}

# A utiliser uniquement si même valeur sur tout l'entierté du bord du domaine !!!

boundary_segments = mesh.get_boundary_segments()
for segment in boundary_segments:
    tag = getattr(segment, 'tag', None)
    value = dirichlet_value
    for node in segment.get_nodes():
        dirichlet_bcs[node.get_ids()] = value
'''

dirichlet_value = 0
dirichlet_bcs = {}
boundary_segments = [seg for seg in mesh.get_segments() if seg.is_boundary()]
bounds = [seg for seg in boundary_segments if ((seg.get_tag() == (str('boundary_2'))) or (seg.get_tag() == str('boundary_3')))]
# print('bounds', bounds, '\n')
'''
for seg in bounds:
    print(seg.get_tag())
'''

for segment in bounds:
    tag = getattr(segment, 'tag', None)
    value = dirichlet_value
    for node in segment.get_nodes():
        dirichlet_bcs[node.get_ids()] = value


# %% Initialiser et exécuter le solveur
solver = FEMSolver(mesh)
solver.assemble_system(k_coefficient=k_coefficient, source_term_func=source_term)
solver.apply_boundary_conditions(dirichlet_bcs=dirichlet_bcs)
solution = solver.solve()

# %% Post-traitement et visualisation

F = ScalarField(mesh, data=solution)
# F.plot(method='scatter')
F.plot()

# plot_mesh(mesh)

boundary_segs = [seg for seg in mesh.get_segments() if seg.is_boundary()]
print(f"Nombre de segments de bord : {len(boundary_segs)}")

'''
for seg in boundary_segs:
    print('\n', seg)
'''
print('\n')

# F.set_field_value(solution)
print('Solutions nodales', F.get_field())
print(len(mesh.get_nodes()))
