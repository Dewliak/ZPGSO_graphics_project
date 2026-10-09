# ZPGSO Render Project

A simple 3D renderer written in python, for ZPGSO class project

## Requirements

- Python 3.11 or newer
- [uv](https://docs.astral.sh/uv/)
- Tkinter
- NumPy


## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/Dewliak/ZPGSO_graphics_project/tree/master
cd zpgso-render-project
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
- **Load OBJ** — load a Wavefront OBJ model.
- **Reset** — reset the model transformation and transformation parameters.
- **Translate** — translate the model along the X, Y, and Z axes.
- **Rotate** — rotate the model around the X, Y, and Z axes. Angles are specified in radians.
- **Scale** — uniformly scale the model using the specified factor.

The GUI displays the number of vertices and faces loaded from the selected model.

## Running tests

Run the unit tests from the project root:

```bash
uv run python -m unittest discover -s tests -v
```

