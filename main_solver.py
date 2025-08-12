from core.geometry.node import Node
from core.geometry.triangle import Triangle
from core.geometry.mesh import Mesh
from visualisation.plot_utils import plot_mesh
from core.elements.p1_element import P1Element

import numpy as np
import matplotlib.pyplot as plt

from core.geometry import square_mesh, GEOMETRY_MAPPING, Geometry
from core.solver import FEMSolver

from core.physics.scalarfield import ScalarField

#%% Création Maillage
h = 1.0 # hauteur
l = 1.0 # largeur
n = 50  # nombre de divisions par côté

# Réinitialiser le registre des nœuds pour s'assurer d'un maillage propre
Node.reset_registry()

mesh = Mesh.from_geometry(Geometry.SQUARE, h=h, l=l, n=n)

#%%
# Coefficient de diffusion
def k_coefficient(x, y):
    return 1.0 # Coefficient constant pour l'exemple

# Terme source
def source_term(x, y):
    # Exemple: f(x,y) = 10
    return 1

#%% Conditions Limites

dirichlet_value = 0
dirichlet_bcs = {}
boundary_segments = mesh.get_boundary_segments()
for segment in boundary_segments:
    tag = getattr(segment, 'tag', None)
    value = dirichlet_value
    for node in segment.get_nodes():
        dirichlet_bcs[node.get_ids()] = value

#%% Initialiser et exécuter le solveur
solver = FEMSolver(mesh)
solver.assemble_system(k_coefficient=k_coefficient, source_term_func=source_term)
solver.apply_boundary_conditions(dirichlet_bcs=dirichlet_bcs)
solution = solver.solve()

#%% Post-traitement et visualisation

F = ScalarField(mesh, solution)
F.plot(method='scatter')
F.plot()



