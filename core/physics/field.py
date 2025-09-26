import numpy as np
import matplotlib.pyplot as plt

from abc import ABC, abstractmethod

from ..geometry.mesh import Mesh

import matplotlib.tri as tri

class Field(ABC):
    FIELD_TYPE = "Generic"
    
    def __init__(self, mesh: Mesh, data=None):
        self._mesh = mesh
        nb_nodes = len(mesh.get_nodes())
        '''
        if data is not None:
            if len(data) != nb_nodes:
                raise ValueError('len(data) doit etre égal au nombre de noeuds.')
                
            dim = len(data[0])
            if any(len(d) != dim for d in data):
                raise ValueError('Toutes le svaleurs aux noeuds doivent avoir le meme nombre de coordonnées !')
            self._data = data
        else:
            self._data = [None]* nb_nodes
        '''
        
        if data is not None:
            if len(data) != nb_nodes:
                raise ValueError("len(data) doit être égal au nombre de noeuds.")
            self._data = data
        else:
            self._data = [0.0] * nb_nodes
            
    
    @property
    def mesh(self):
        return self._mesh
    
    @property 
    def data(self):
        return self._data


    

