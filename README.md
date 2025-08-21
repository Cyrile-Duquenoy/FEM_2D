# FEM_2D

Implémentation **from scratch** d’une méthode des éléments finis (FEM) en 2D,  
résolvant le problème de Poisson avec second membre `f = 1` et conditions de Dirichlet sur les bords.

---

## Objectif
- Créer un solveur FEM pédagogique et modulaire en Python.
- Permettre une comparaison simple avec un solveur existant (**FreeFem**).
- Offrir une architecture claire et extensible pour d’autres problèmes physiques.

## 📊 Comparaison avec FreeFem

<div style="display: flex; gap: 20px;">
  <img src="images/sol_python.png" alt="Résultat FEM 2D" width="400" height="300">
  <img src="images/sol_FreeFem.png" alt="Résultat FreeFem 2D" width="400" height="300">
</div>

## Convergence

Test réalisé en prenant $f(x,y)=2 \pi^2 sin(\pi x)sin(\pi y)$  


<div style="display: flex; gap: 20px;">
  <img src="images/convergence.png" alt="Résultat FEM 2D" width="400" height="300">
</div>

