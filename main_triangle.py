import numpy as np
import matplotlib.pyplot as plt

from core.geometry.triangle import Triangle
from core.geometry.node import Node

n1, n2, n3 = Node(0,0, ids=1), Node(1,0, ids=2), Node(0,1, ids=3)

Tref = Triangle(n1, n2, n3, ids=1)

print(Tref)

def phi(x, y, i):
    if i == 1:
        return 1 - x - y
    elif i == 2:
        return x
    elif i == 3:
        return y  # Corrigé ici

def grad_phi(i):
    if i == 1:
        return np.array([-1, -1])
    elif i == 2:
        return np.array([1, 0])
    elif i == 3:
        return np.array([0, 1])

print(grad_phi(1))  # Affiche [-1 -1]
print(grad_phi(2))  # Affiche [1 0]
print(grad_phi(3))  # Affiche [0 1]





# Noeuds du triangle physique
x1, y1 = n1.get_coord()[0], n1.get_coord()[1]
x2, y2 = n2.get_coord()[0], n2.get_coord()[1]
x3, y3 = n3.get_coord()[0], n3.get_coord()[1]

B = np.array([[x2 - x1, x3 - x1],
              [y2 - y1, y3 - y1]])

invB_T = np.linalg.inv(B).T

def grad_phi_ref(i):
    if i == 1:
        return np.array([-1, -1])
    elif i == 2:
        return np.array([1, 0])
    elif i == 3:
        return np.array([0, 1])

def grad_phi_phys(i):
    grad_ref = grad_phi_ref(i)
    return invB_T @ grad_ref

for i in [1, 2, 3]:
    print(f"Gradient de phi_{i} sur T : {grad_phi_phys(i)}")
