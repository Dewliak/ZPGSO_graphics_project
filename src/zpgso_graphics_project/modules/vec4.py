from __future__ import annotations
import numpy
from math import sqrt
class Vec4:
    def __init__(self,
                 x:float,
                 y:float,
                 z:float,
                 w:float=1.0):
        
        self._vector = numpy.array([x,y,z,w], dtype=float)

    def normalize(self, other:Vec4):
        """
        n = (self x other) => N = n/|n|

        cross product is defined as: 

        a x b
        """
        return 

    def __sub__(self, other: Vec4) -> Vec4:
        if not isinstance(other,Vec4):
            raise ValueError("Vec4 -: you can only subs an other Vec4")

        return Vec4(
            self._vector[0] - other._vector[0],
            self._vector[1] - other._vector[1],
            self._vector[2] - other._vector[2],
            self._vector[3] - other._vector[3],
        )



    def __getitem__(self, key:int) -> float:
        return self._vector[key]

    def __repr__(self) -> str:
        x, y, z, w = self._vector
        return f"Vec4({x:.2f}, {y:.2f}, {z:.2f}, {w:.2f})"

    
def euclidean_distance(p: Vec4, q: Vec4) -> float:
    if p._vector[3] != 1 or q._vector[3] != 1: 
          raise ValueError("euclidiean distance: p,q has to be points, w=1")
    
    return sqrt((p[0]-q[0])**2 + (p[1]-q[1])**2 + (p[2]-q[2])**2 )              

def cross_product(v: Vec4,w: Vec4) -> Vec4:
    if v._vector[3] != 0 or w._vector[3] != 0:
        raise ValueError("Vec4 - cross_product : v,w has to be vector, w=0 ")

    x,y,z = v._vector[:3]
    a,b,c = w._vector[:3]

    return Vec4(
         y*c - z*b,
         z*a - x*c,
         x*b - y*a,
        0
    )

def dot_product(v: Vec4, w: Vec4) -> float:
    if v._vector[3] != 0 or w._vector[3] != 0:
            raise ValueError("Vec4 - dot_product : v,w has to be vector, w=0 ")
    
    return v[0]*w[0] + v[1]*w[1] + v[2]*w[2]


def normalize(v: Vec4) -> Vec4:
    if v._vector[3] != 0:
            raise ValueError("Vec4 - normalize : v, w=0 ")

    size = sqrt(v._vector[0]*v._vector[0] + v._vector[1]*v._vector[1] + v._vector[2]*v._vector[2])

    return Vec4(v._vector[0]/size,
                v._vector[1]/size,
                v._vector[2]/size,
                0)

    