import numpy

class Vec4:
    def __init__(self,
                 x:float,
                 y:float,
                 z:float,
                 w:float=1.0):
        
        self._vector = numpy.array([x,y,z,w], dtype=float)

    def __getitem__(self, key:int) -> float:
        return self._vector[key]

    def __repr__(self) -> str:
        x, y, z, w = self._vector
        return f"Vec4({x:.2f}, {y:.2f}, {z:.2f}, {w:.2f})"

    
