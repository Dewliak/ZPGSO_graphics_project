from typing import List, Tuple

from .vec4 import Vec4


class IndexedFace:
    def __init__(
        self,
        vertices: list[Vec4],
        indices: List[Tuple[int, int, int]]):

        self._vertices = vertices
        self._indices = indices

    def get_vertices(self) -> list[Vec4]:
        return self._vertices

    def get_faces(self) ->  List[Tuple[int, int, int]]:
        return self._indices

    