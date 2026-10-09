from typing import List

from modules.vec4 import Vec4
from modules.mat4 import Mat4

import numpy as np
import math

# full Pixel = V_p*O*C*M*P
"""
V_p - is point ot pixel
O - is orthograpich matrix
"""
# Affine transformation matrices
def get_identity_matrix():
     return Mat4(Vec4(1        ,0      ,0      ,0),
                 Vec4(0        ,1      ,0      ,0),
                 Vec4(0        ,0      ,1      ,0),
                 Vec4(0        ,0      ,0      ,1))


def get_rotation_z_axis_matrix(phi: float):
    return Mat4(Vec4(math.cos(phi)        ,-math.sin(phi)      ,0      ,0),
                Vec4(math.sin(phi)        ,math.cos(phi)       ,0      ,0),
                Vec4(0                    ,0                   ,1      ,0),
                Vec4(0                    ,0                   ,0      ,1))


def get_rotation_y_axis_matrix(phi:float):         
     return Mat4(Vec4(math.cos(phi)        ,0      ,math.sin(phi)      ,0),
                 Vec4(0                    ,1      ,0                  ,0),
                 Vec4(-math.sin(phi)       ,0      ,math.cos(phi)      ,0),
                 Vec4(0                    ,0      ,0                  ,1))


def get_rotation_x_axis_matrix(phi:float):         
     return Mat4(Vec4(1        ,0                  ,0                   ,0),
                 Vec4(0        ,math.cos(phi)      ,-math.sin(phi)      ,0),
                 Vec4(0        ,math.sin(phi)      ,math.cos(phi)       ,0),
                 Vec4(0        ,0                  ,0                   ,1))


def get_translation_matrix(tx:float, ty:float, tz:float):         
     return Mat4(Vec4(1        ,0      ,0      ,tx),
                 Vec4(0        ,1      ,0      ,ty),
                 Vec4(0        ,0      ,1      ,tz),
                 Vec4(0        ,0      ,0      , 1))


def get_scaling_matrix(sx:float, sy:float, sz:float):         
     return Mat4(Vec4(sx        ,0       ,0       ,0),
                 Vec4(0         ,sy      ,0       ,0),
                 Vec4(0         ,0       ,sz      ,0),
                 Vec4(0         ,0       ,0       ,1))


# Rendering matrixes
def get_camera_transformation_matrix(camera_pos:Vec4):
    #C - view, camera at (x,y,z)
    return Mat4(Vec4(1      ,0      ,0      ,-camera_pos[0]),
                Vec4(0      ,1      ,0      ,-camera_pos[1]),
                Vec4(0      ,0      ,1      ,-camera_pos[2]),
                Vec4(0      ,0      ,0      ,             1),
                )

def get_orthographic_transformation_matrix(left:float, right:float, top:float, bottom:float):
    # O 
        return Mat4(Vec4(2/(right - left),0             ,0             ,0),
                    Vec4(0               ,2/(top-bottom),0             ,0),
                    Vec4(0               ,0             ,0             ,0),
                    Vec4(0               ,0             ,0             ,1),
                    )

def get_pixel_transformation_matrix(W: int, H: int):
      #V_p
    return Mat4(Vec4(W/2        ,0      ,0      ,W/2),
                Vec4(0          ,-H/2   ,0      ,H/2),
                Vec4(0          ,0      ,1      ,  0),
                Vec4(0          ,0      ,0      ,  1),
                )



def combine_transformation_matrices(transformations: List[Mat4]) -> Mat4:
    # We are combining backwards so it visually corressponds to the math writing
    # e.g: OTMP will be in format [O, T, M, P], and first X = M*P,  X' = T*X, X'' = O*X'
    # we dont have to do any check since all matrices are 4x4
    X = transformations[-1]
    for i in range(len(transformations)-2, -1,-1):
         X = transformations[i]*X

    return X
         
