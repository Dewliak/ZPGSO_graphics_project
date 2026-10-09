## 2.1. Stage 1: Loading + Transformations
Load a mesh from an OBJ file and show it as a wireframe. The user can translate, rotate
and scale it; all transformations are 4×4 matrices that you multiply.

I. Types. Vec4 (x, y, z, w), Mat4 (4×4) and IndexedFace: an array of Vec4 vertex
positions (w = 1) and an array of integer indices (3 per triangle). Multiply(Mat4,
Mat4) and Multiply(Mat4, Vec4), or an overloaded *.

II. Loader. The Load button reads the v and f lines of an OBJ file (ignore other lines;
accept f a/b/c by taking the first number). Show the vertex and face counts. A
broken file gives a message, not a crash.

III. Wireframe. Draw every edge of every triangle (no fill, Z ignored) with the model’s
origin at the center of the drawing area like Img1 and Img2.

IV. Controls. Load and Reset; three number fields plus Translate; three number fields
plus Rotate (radians about X, Y, Z); one number field plus Scale. The layout is free.


## 2.2. Stage 2: Shading + Lighting
Extend Stage 1: show the model solid, remove faces that point away from the viewer, and
color each face with the Blinn–Phong model. Loading, transformations and reset must
keep working, and the shading must update when the model is transformed.


I. Normals. For each triangle, N = normalize((v1 − v0) × (v2 − v0)), computed from
the transformed vertices M · v.

II. Back-face culling. Draw a face only if N · V > 0 with V = (0, 0, 1), that is, N_z > 0.
Decide this in 3D, before projection and before the Y flip.

III. Solid faces. Each remaining face is a filled polygon of one color, with no outline
(scr1, scr2).

IV. Lighting. Color = base color × intensity I (as the Blinn–Phong model describes),
clamped to 0 … 255 per channel.

V. Light control. Three number fields for a direction d and a Set Light Direction
button; redraw when it changes. The light is fixed in the scene and does not rotate
with the model.


## 2.3. Bonus (optional, submitted with Stage 2; say in your README which you
did)
✓ Material properties (+5 %): ka, kd, ks, shininess and base color editable in the
GUI, re-rendering on change.
✓ Lighting model switch (+10 %): Phong vs Blinn–Phong. Phong uses R = 2(N·L)N −
L and max(0, R·V)^n instead of (N·H)^n.
✓ Light types (+15 %): switch between a directional light (direction) and a point light
(position; the GUI text changes accordingly). For a point light L = normalize(P_light
− C), with C the center of the face