'''
import numpy as np

from .mesh import Mesh
from .node import Node
from .segment import Segment


class Boundary:
    def __init__(self, mesh: Mesh):
        self._mesh = mesh
        self._segments = [seg for seg in mesh.get_segments() if seg.is_boundary()]

    def get_all_segments(self) -> list[Segment]:
        return self._segments

    def get_segments_by_tag(self, tag: str) -> list[Segment]:
        return [seg for seg in self._segments if seg.get_tag() == tag]

    def get_available_tags(self) -> list[str]:
        return sorted(set(seg.get_tag() for seg in self._segments if seg.get_tag() is not None))

    def get_total_length_by_tag(self, tag: str) -> float:
        return sum(seg.get_length() for seg in self.get_segments_by_tag(tag))

    def get_coordinates_by_tag(self, tag: str) -> list[tuple[float, float]]:
        coords = []
        for seg in self.get_segments_by_tag(tag):
            for node in seg.get_nodes():
                coord = node.get_coord()
                if coord not in coords:  # évite les doublons
                    coords.append(coord)
        return coords
'''