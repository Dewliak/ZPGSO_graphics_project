from zpgso_render_project.modules.vec4 import Vec4
from zpgso_render_project.modules.mat4 import Mat4
from zpgso_render_project.modules.indexed_face import IndexedFace
from zpgso_render_project.modules.loader import load_obj_file

from zpgso_render_project.modules.transformation_matrices import *


import numpy as np



vertices, faces = load_obj_file("obj_files/bunny.obj")


print(len(vertices))
print(len(faces))

indexed_faces = IndexedFace(vertices, faces)

# Parameters


"""
# Step  Result
1 local (1, 1, 1)
2 model, T(5,0,0)·S(2) (7, 2, 2)
3 view, camera at (0,0,10) (7, 2, −8)
4 orthographic, window ±10 × ±7.5 (0.7, 0.267)
5 800×600 viewport,Y flipped pixel (680, 220)
"""
"
P = Vec4(1,1,1)
scale = 2
translation = (5,0,0)
camera = Vec4(0,0,10)
window_r = 10
window_l = 10
window_t = 7.5
window_b = 7.5
W = 800
H = 600






object_transformations = combine_transformation_matrices([
    get_translation_matrix(tx=translation[0],ty=translation[1],tz=translation[2]),
    get_scaling_matrix(scale,scale,scale)
    
])



world_transformation = combine_transformation_matrices([
    get_pixel_transformation_matrix(W,H), # pixel conversion
    get_orthographic_transformation_matrix(-window_l,window_r,window_t, -window_b), # ortographic projection
    get_camera_transformation_matrix(camera_pos=camera), # transform for camera
    ])



full_pipeline = combine_transformation_matrices([world_transformation, object_transformations, P])

"