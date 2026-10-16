# ZPGSO Render Project

A simple 3D renderer written in python, for ZPGSO class project

## Project solution

1. Created the neccessary Mat4, Vec4 and IndexedFaces types, later extended them a bit with neccesary operations for shading
2. Created the transformations matrices, and also with the help of combine_transformation_matrices(transformations: List[Mat4]), a first projection pipeline was built out. In gui rendered with lines
3. Added controls for transformation and reset
4. extended Vec4, with normalize, cross_product, dot_product, and some operations inside Vec4
5. Implemented back_culling with V = (0,0,1)
6. Polygon, with color calculated from the center of the polygon with lightning, conventions used are commented inside modules/light_type.py
7. Implemented the Blinn-Phong and Phong model + switch to swtich between them
8. Added light controls for directional and point light
9. Added material parameters in the model


# Bonuses solved
✓ Material properties (+5 %)
✓ Lighting model switch (+10 %)
✓ Light types (+15 %)

## Requirements

- Python 3.11 or newer
- [uv](https://docs.astral.sh/uv/)
- Tkinter
- NumPy


## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/Dewliak/ZPGSO_graphics_project/tree/master
cd zpgso-graphics-project
```

Install the project dependencies:

```bash
uv sync
```

## Running the application

From the project root directory, run:

```bash
uv run main.py
```

The GUI will open in a separate window. Click **Load OBJ** to select a `.obj` model file. Example models are available in the `obj_files/` directory.

## Controls
- **Load OBJ** - load a Wavefront OBJ model.
- **Reset** - reset the model transformation and transformation parameters.
- **Translate** - translate the model along the X, Y, and Z axes.
- **Rotate** - rotate the model around the X, Y, and Z axes. Angles are specified in radians.
- **Scale** - uniformly scale the model using the specified factor.
- **Material** - Change k_a, k_d, k_s and the specular exponent ( based on the Blinn-Phong model)
- **Change light type** - directional/point light and neccsary parameters
- **Shadowing mode** - Phong/Blinn-Phong model
- **Wireframe On/Off**

The GUI displays the number of vertices and faces loaded from the selected model.

## Running tests

Run the unit tests from the project root:

```bash
uv run python -m unittest discover -s tests -v
```

