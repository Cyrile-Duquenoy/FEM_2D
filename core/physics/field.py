from abc import ABC

from ..geometry.mesh import Mesh


class Field(ABC):
    FIELD_TYPE = "Generic"

    def __init__(self, mesh: Mesh, data=None):
        self._mesh = mesh
        nb_nodes = len(mesh.get_nodes())

        if data is not None:
            if len(data) != nb_nodes:
                raise ValueError("len(data) doit être égal\
                                 au nombre de noeuds.")
            self._data = data
        else:
            self._data = [0.0] * nb_nodes

        self.field = self._create_field()

    @property
    def mesh(self):
        return self._mesh

    @property
    def data(self):
        return self._data

    def _create_field(self):
        field = {}
        nodes = self._mesh.get_nodes()
        for i, node in enumerate(nodes):
            field[node.ids] = self._data[i]
        return field

    def get_field(self):
        return self.field
