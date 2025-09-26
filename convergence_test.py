from core.geometry.node import Node
from core.geometry.triangle import Triangle
from core.geometry.mesh import Mesh
from core.elements.p1_element import P1Element
from core.solver import FEMSolver
from core.physics.scalarfield import ScalarField
from core.geometry import Geometry


import numpy as np
import matplotlib.pyplot as plt

# --- solution exacte et source ---
def u_exact(x, y):
    return np.sin(np.pi*x) * np.sin(np.pi*y)

def grad_u_exact(x, y):
    return np.array([np.pi*np.cos(np.pi*x)*np.sin(np.pi*y),
                     np.pi*np.sin(np.pi*x)*np.cos(np.pi*y)])

def f_source(x, y):
    return 2*np.pi**2 * np.sin(np.pi*x) * np.sin(np.pi*y)

# --- gradient P1 sur un triangle (constant par élément) ---
def element_grad_P1(element: Triangle, U, node_to_idx):
    nodes = element.get_nodes()
    coords = np.array([node.get_coord() for node in nodes])
    values = np.array([U[node_to_idx[n.get_ids()]] for n in nodes])
    A = np.column_stack((np.ones(3), coords))
    a, b, c = np.linalg.solve(A, values)
    return np.array([b, c])

# --- erreur H1 semi-norme ---
def h1_seminorm_error(field: ScalarField):
    mesh = field._mesh
    U = field._data
    node_to_idx = {node.get_ids(): i for i, node in enumerate(mesh.get_nodes())}
    err2 = 0.0

    for el in mesh.get_elements():
        if isinstance(el, Triangle):
            grad_uh = element_grad_P1(el, U, node_to_idx)
            # centroid pour évaluer la solution exacte
            centroid = np.mean([n.get_coord() for n in el.get_nodes()], axis=0)
            grad_ex = grad_u_exact(*centroid)
            diff = grad_uh - grad_ex
            area = P1Element(el).area
            err2 += area * np.dot(diff, diff)
    
    return np.sqrt(err2)

# --- erreur L2 ---
def l2_error(field: ScalarField):
    """Erreur L2 entre le champ scalaire et la solution exacte"""
    mesh = field._mesh
    U = field._data
    node_to_idx = {node.get_ids(): i for i, node in enumerate(mesh.get_nodes())}
    
    err2 = 0.0
    for el in mesh.get_elements():
        if isinstance(el, Triangle):
            uh_vals = np.array([U[node_to_idx[n.get_ids()]] for n in el.get_nodes()])
            coords = np.array([n.get_coord() for n in el.get_nodes()])
            # centroid pour évaluer la solution exacte
            centroid = np.mean(coords, axis=0)
            u_ex = u_exact(*centroid)
            # interpolation P1 au centroid
            uh_centroid = np.mean(uh_vals)
            area = P1Element(el).area
            err2 += area * (uh_centroid - u_ex)**2
    return np.sqrt(err2)

# --- boucle de convergence ---
n_list = [5, 10, 15, 20, 25, 30, 40]
H1_errors = []
L2_errors = []

for n in n_list:
    Node.reset_registry()
    Triangle.reset_registry()
    
    mesh = Mesh.from_geometry(Geometry.SQUARE, h=1.0, l=1.0, n=n)
    
    # Dirichlet BC
    dirichlet_bcs = {}
    for seg in mesh.get_boundary_segments():
        for node in seg.get_nodes():
            x, y = node.get_coord()
            dirichlet_bcs[node.get_ids()] = u_exact(x, y)
    
    solver = FEMSolver(mesh)
    solver.assemble_system(k_coefficient=1.0, source_term_func=f_source)
    solver.apply_boundary_conditions(dirichlet_bcs)
    U_num = solver.solve()
    
    eH1 = h1_seminorm_error(ScalarField(mesh, U_num))
    eL2 = l2_error(ScalarField(mesh, U_num))
    
    H1_errors.append(eH1)
    L2_errors.append(eL2)
    
    print(f"n={n}, |e|_H1 ≈ {eH1:.6f}, |e|_L2 ≈ {eL2:.6f}")

# --- ordre de convergence ---
print("\nOrdres de convergence H1 :")
for i in range(len(n_list)-1):
    p = np.log(H1_errors[i] / H1_errors[i+1]) / np.log(n_list[i+1] / n_list[i])
    print(f"n={n_list[i]} -> n={n_list[i+1]} : {p:.3f}")

print("\nOrdres de convergence L2 :")
for i in range(len(n_list)-1):
    p = np.log(L2_errors[i] / L2_errors[i+1]) / np.log(n_list[i+1] / n_list[i])
    print(f"n={n_list[i]} -> n={n_list[i+1]} : {p:.3f}")

# --- visualisation convergence ---
plt.figure(figsize=(8,6))
plt.loglog(n_list, H1_errors, 's-', label='Erreur H¹ semi-norme')
plt.loglog(n_list, L2_errors, 'o-', label='Erreur L²')
plt.loglog(n_list, H1_errors[0]*(n_list[0]/np.array(n_list))**1, '--', color='gray', label='Ordre H1 ≈ 1')
plt.loglog(n_list, L2_errors[0]*(n_list[0]/np.array(n_list))**2, '--', color='black', label='Ordre L2 ≈ 2')
plt.xlabel('n (divisions par côté)')
plt.ylabel('Erreur')
plt.title('Convergence FEM P1')
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend()
plt.show()





