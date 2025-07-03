import matplotlib.pyplot as plt
from core.mesh import Mesh
from typing import Optional, List, Tuple
from matplotlib.axes import Axes

def plot_mesh(mesh, highlight_segment=None, show_ids=True, ax=None, title="Maillage triangulaire"):
    """
    Affiche un maillage triangulaire à partir d'un objet Mesh.

    Args:
        mesh (Mesh): Objet Mesh contenant les triangles.
        highlight_segment (Segment, optional): Segment à mettre en évidence.
        show_ids (bool): Affiche les IDs des nœuds si True.
        ax (matplotlib.axes.Axes, optional): Axes matplotlib sur lesquels dessiner.
        title (str): Titre de la figure.
    """
    created_fig = False
    if ax is None:
        fig, ax = plt.subplots()
        created_fig = True

    elements = mesh.get_elements()

    for triangle in elements:
        coords = [node.get_coord() for node in triangle.get_nodes()]
        coords.append(coords[0])  # boucle fermée
        xs, ys = zip(*coords)
        ax.plot(xs, ys, 'k-', linewidth=1)

        if show_ids:
            for node in triangle.get_nodes():
                x, y = node.get_coord()
                ax.text(x, y, str(node.get_ids()), color='blue', fontsize=10, ha='right')

    if highlight_segment:
        n1, n2 = highlight_segment.get_nodes()
        x1, y1 = n1.get_coord()
        x2, y2 = n2.get_coord()
        ax.plot([x1, x2], [y1, y2], 'r-', linewidth=3, label="Segment sélectionné")

    ax.set_aspect('equal')
    ax.set_title(title)
    ax.grid(True)
    if highlight_segment:
        ax.legend()
    if created_fig:
        plt.show()


