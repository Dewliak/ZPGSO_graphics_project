import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from pathlib import Path
from typing import Tuple, List

from .loader import load_obj_file
from .mat4 import Mat4
from .vec4 import Vec4, normalize, cross_product, dot_product
from .transformation_matrices import *
from .indexed_face import IndexedFace

from .utilities import rgb_to_hex

from .material import Material
from .light_types import DirectionalLightSource, PointLightSource
from .lightning_model import BlinnPhongModel, PhongModel


SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 760

# PARAMETERS
LINE_WIDTH = 1
WIDTH = 900
HEIGHT = 500

CAMERA_POSITION = Vec4(0, 0, 0)
WINDOW_R = 10
WINDOW_L = 10
WINDOW_T = 7.5
WINDOW_B = 7.5

WIREFRAME = False

OBJECT_TRANSFORMATION = get_identity_matrix()
VIEW_TRANSFORMATION = combine_transformation_matrices([
    get_camera_transformation_matrix(camera_pos=CAMERA_POSITION),  # transform for camera
])
PROJECTION_TRANSFORMATION = combine_transformation_matrices([
    get_pixel_transformation_matrix(WIDTH, HEIGHT),  # pixel conversion
    get_orthographic_transformation_matrix(-WINDOW_L, WINDOW_R, WINDOW_T, -WINDOW_B),  # orthographic projection
])


default_blue = Material(
    color=(50, 100, 220),
    K_A=0.15,
    K_D=0.75,
    K_S=0.35,
    specular_exponent=32,
)

default_point_light = PointLightSource(
    position=Vec4(0, -1, 0, 1.0),
    intensity=1,
    k_c=1,
    k_l=0.02,
    k_q=0.002,
)
VIEW_DIRECTION = Vec4(0.0, 0.0, 1.0, 0.0)


class RendererGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("3D Renderer")
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.minsize(600, 400)

        self.filename = tk.StringVar(value="No file loaded")
        self.vertex_count = tk.StringVar(value="Vertices (v): 0")
        self.face_count = tk.StringVar(value="Faces (f): 0")

        self.vertices = []
        self.faces = []
        self.indexed_face = None

        self.shader_model = BlinnPhongModel()
        self.material = default_blue
        self.light = default_point_light
        self.base_color = (50, 100, 220)

        # Top toolbar
        toolbar = tk.Frame(root, padx=10, pady=10)
        toolbar.pack(fill="x")

        top_row = tk.Frame(root)
        top_row.pack(fill="x", padx=10, pady=5)

        controls = tk.LabelFrame(top_row, text="Transformations", padx=10, pady=8)
        controls.pack(side="left", fill="y")

        self.build_material_panel(top_row)

        # Translation
        tk.Label(controls, text="Translate (X, Y, Z):").grid(row=0, column=0, padx=5)
        self.tx = tk.Entry(controls, width=7)
        self.tx.insert(0, "0")
        self.tx.grid(row=0, column=1)

        self.ty = tk.Entry(controls, width=7)
        self.ty.insert(0, "0")
        self.ty.grid(row=0, column=2)

        self.tz = tk.Entry(controls, width=7)
        self.tz.insert(0, "0")
        self.tz.grid(row=0, column=3)

        tk.Button(controls, text="Translate", command=self.translate).grid(row=0, column=4, padx=10)

        # Rotation
        tk.Label(controls, text="Rotate (X, Y, Z) rad:").grid(row=1, column=0, padx=5)
        self.rx = tk.Entry(controls, width=7)
        self.rx.insert(0, "0")
        self.rx.grid(row=1, column=1)

        self.ry = tk.Entry(controls, width=7)
        self.ry.insert(0, "0")
        self.ry.grid(row=1, column=2)

        self.rz = tk.Entry(controls, width=7)
        self.rz.insert(0, "0")
        self.rz.grid(row=1, column=3)

        tk.Button(controls, text="Rotate", command=self.rotate).grid(row=1, column=4, padx=10)

        # Uniform scaling
        tk.Label(controls, text="Scale:").grid(row=2, column=0, padx=5)
        self.scale = tk.Entry(controls, width=7)
        self.scale.insert(0, "1")
        self.scale.grid(row=2, column=1)

        tk.Button(controls, text="Scale", command=self.scale_model).grid(row=2, column=4, padx=10)

        tk.Button(toolbar, text="Load OBJ", command=self.load_file, padx=15).pack(side="left")
        tk.Button(toolbar, text="Reset", command=self.reset, padx=15).pack(side="left", padx=5)

        tk.Label(toolbar, textvariable=self.filename, anchor="w").pack(side="left", padx=15, fill="x", expand=True)

        tk.Label(
            toolbar, textvariable=self.vertex_count, font=("TkDefaultFont", 11, "bold"),
        ).pack(side="left", padx=(0, 30))

        tk.Label(
            toolbar, textvariable=self.face_count, font=("TkDefaultFont", 11, "bold"),
        ).pack(side="left")

        # Body: canvas on the left, lighting panel on the right
        body = tk.Frame(root)
        body.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        self.canvas = tk.Canvas(
            body,
            width=WIDTH,
            height=HEIGHT,
            background="#20242b",
            highlightthickness=0,
        )
        self.canvas.pack(side="left", anchor="n")

        self.build_lighting_panel(body)

        self.canvas.create_text(
            20, 20,
            text="Load an OBJ file to begin",
            fill="white",
            anchor="nw",
            tags="placeholder",
        )

    # ------------------------------------------------------------------
    # Lighting / material panel
    # ------------------------------------------------------------------
    def _slider(self, parent, label, row, from_, to, resolution, default, col=0, length=170):
        """Label + horizontal slider on one grid cell pair. Returns the tk.DoubleVar."""
        var = tk.DoubleVar(value=default)
        tk.Label(parent, text=label, anchor="w").grid(row=row, column=col * 2, sticky="w", padx=(8 if col else 0, 2))
        scale = tk.Scale(
            parent,
            variable=var,
            from_=from_,
            to=to,
            resolution=resolution,
            orient="horizontal",
            length=length,
            command=lambda _v: self.on_param_change(),
        )
        scale.grid(row=row, column=col * 2 + 1, sticky="ew")
        var.scale = scale # type: ignore  # keep the widget so it can be enabled/disabled 
        return var

    def build_lighting_panel(self, parent):
        panel = tk.Frame(parent)
        panel.pack(side="left", fill="y", padx=(10, 0), anchor="n")

        # ---------------- Light ----------------
        light_box = tk.LabelFrame(panel, text="Light", padx=8, pady=4)
        light_box.pack(fill="x")

        self.light_type_var = tk.StringVar(value="Point")
        type_row = tk.Frame(light_box)
        type_row.grid(row=0, column=0, columnspan=2, sticky="w")
        tk.Radiobutton(type_row, text="Directional", variable=self.light_type_var,
                       value="Directional", command=self.on_light_type_change).pack(side="left")
        tk.Radiobutton(type_row, text="Point", variable=self.light_type_var,
                       value="Point", command=self.on_light_type_change).pack(side="left")

        self.light_vec_label = tk.Label(light_box, text="Position (X, Y, Z):")
        self.light_vec_label.grid(row=1, column=0, columnspan=2, sticky="w")

        p = default_point_light.position
        self.light_x = self._slider(light_box, "X", 2, -20, 20, 0.1, p[0])
        self.light_y = self._slider(light_box, "Y", 3, -20, 20, 0.1, p[1])
        self.light_z = self._slider(light_box, "Z", 4, -20, 20, 0.1, p[2])
        self.light_intensity = self._slider(light_box, "Intensity", 5, 0, 5, 0.05, default_point_light.intensity)

        self.k_c = self._slider(light_box, "kc", 6, 0, 2, 0.01, default_point_light.k_c)
        self.k_l = self._slider(light_box, "kl", 7, 0, 0.5, 0.001, default_point_light.k_l)
        self.k_q = self._slider(light_box, "kq", 8, 0, 0.1, 0.0001, default_point_light.k_q)

        self.atten_vars = [self.k_c, self.k_l, self.k_q]

        self.set_light_btn = tk.Button(light_box, text="Set Light Position", command=self.on_param_change)
        self.set_light_btn.grid(row=9, column=0, columnspan=2, pady=4)

        # ---------------- Shading model / display ----------------
        misc_box = tk.LabelFrame(panel, text="Shading", padx=8, pady=4)
        misc_box.pack(fill="x", pady=(8, 0))

        # on = Blinn-Phong, off = Phong
        self.blinn_var = tk.BooleanVar(value=True)
        self.blinn_switch = tk.Checkbutton(
            misc_box,
            text="Blinn-Phong: ON",
            variable=self.blinn_var,
            indicatoron=False,
            width=18,
            command=self.on_param_change,
        )
        self.blinn_switch.pack(anchor="w", pady=2)

        self.wireframe_var = tk.BooleanVar(value=WIREFRAME)
        tk.Checkbutton(misc_box, text="Wireframe", variable=self.wireframe_var,
                       command=self.on_param_change).pack(anchor="w")

        self.on_light_type_change(redraw=False)

    def build_material_panel(self, parent):
        mat_box = tk.LabelFrame(parent, text="Material", padx=8, pady=4)
        mat_box.pack(side="left", fill="y", padx=(10, 0))

        # 2x2 grid of sliders so it matches the height of the transformations box
        self.m_ka = self._slider(mat_box, "ka", 0, 0, 1, 0.01, default_blue.K_A, col=0, length=120)
        self.m_kd = self._slider(mat_box, "kd", 0, 0, 1, 0.01, default_blue.K_D, col=1, length=120)
        self.m_ks = self._slider(mat_box, "ks", 1, 0, 1, 0.01, default_blue.K_S, col=0, length=120)
        self.m_shininess = self._slider(mat_box, "n", 1, 1, 256, 1, default_blue.specular_exponent, col=1, length=120)

        color_row = tk.Frame(mat_box)
        color_row.grid(row=2, column=0, columnspan=4, sticky="w", pady=(4, 0))
        tk.Label(color_row, text="Base color").pack(side="left")
        self.color_swatch = tk.Label(color_row, width=4, bg=rgb_to_hex(self.base_color), relief="solid") # type: ignore
        self.color_swatch.pack(side="left", padx=6)
        tk.Button(color_row, text="Pick...", command=self.pick_color).pack(side="left")

    def on_light_type_change(self, redraw=True):
        light_type = self.light_type_var.get()
        directional = light_type == "Directional"
        for v in self.atten_vars:  # attenuation: point light only
            v.scale.config(state="disabled" if directional else "normal")
        self.light_vec_label.config(text="Direction (X, Y, Z):" if directional else "Position (X, Y, Z):")
        self.set_light_btn.config(text="Set Light Direction" if directional else "Set Light Position")
        if redraw:
            self.on_param_change()

    def pick_color(self):
        result = colorchooser.askcolor(color=rgb_to_hex(self.base_color), parent=self.root, title="Base color") # type: ignore
        if result and result[0]:
            self.base_color = tuple(int(c) for c in result[0])
            self.color_swatch.config(bg=rgb_to_hex(self.base_color)) # type: ignore
            self.on_param_change()

    def collect_parameters(self) -> dict:
        return {
            # light
            "light_type": self.light_type_var.get(),        # "Directional" or "Point"
            "light_vector": (self.light_x.get(), self.light_y.get(), self.light_z.get()),  # direction or position
            "light_intensity": self.light_intensity.get(),
            "k_c": self.k_c.get(),                          # attenuation (point light only)
            "k_l": self.k_l.get(),
            "k_q": self.k_q.get(),
            # material
            "ka": self.m_ka.get(),
            "kd": self.m_kd.get(),
            "ks": self.m_ks.get(),
            "shininess": self.m_shininess.get(),
            "base_color": self.base_color,                  # (r, g, b) ints
            # shading
            "blinn_phong": self.blinn_var.get(),            # True = Blinn-Phong, False = Phong
            "wireframe": self.wireframe_var.get(),
        }

    def on_param_change(self):
        if not hasattr(self, "wireframe_var"):  # UI still being built
            return
        self.blinn_switch.config(text="Blinn-Phong: ON" if self.blinn_var.get() else "Phong (Blinn OFF)")
        self.update_parameters(self.collect_parameters())
        self.draw_objects()

    def update_parameters(self, params: dict):
        """
        Called on every slider / button / radio change.
        Apply `params` to self.light, self.material, self.shader_model, WIREFRAME, ...
        (draw_objects() is called automatically afterwards.)
        """
        global WIREFRAME
        self.material = Material(params["base_color"],
                                         params["kd"],
                                         params["ks"],
                                         params["ka"],
                                         params["shininess"],)

        if params["blinn_phong"]: # True = Blinn-Phong, False = Phong
            self.shader_model = BlinnPhongModel()
        else:
            self.shader_model = PhongModel()
 
        """
                    "light_vector": (self.light_x.get(), self.light_y.get(), self.light_z.get()),  # direction or position
            "light_intensity": self.light_intensity.get(),
            "k_c": self.k_c.get(),                          # attenuation (point light only)
            "k_l": self.k_l.get(),
            "k_q": self.k_q.get(),
        """
        
        
        if(params["light_type"] == "Point"):
            position = Vec4(params["light_vector"][0],params["light_vector"][1],params["light_vector"][2],1)
            self.light = PointLightSource(
                intensity=params["light_intensity"],
                position=position,
                k_c=params["k_c"],
                k_l=params["k_l"],
                k_q=params["k_q"],
            )


        elif(params["light_type"] == "Directional"):
            direction = Vec4(params["light_vector"][0],params["light_vector"][1],params["light_vector"][2],1)
            self.light = DirectionalLightSource(
                intensity=params["light_intensity"],
                direction=direction,
            )

        
        WIREFRAME = params["wireframe"]

    # ------------------------------------------------------------------
    # File loading
    # ------------------------------------------------------------------
    def load_file(self):
        path = filedialog.askopenfilename(
            parent=self.root,
            title="Select OBJ file",
            filetypes=[
                ("Wavefront OBJ files", "*.obj"),
                ("All files", "*.*"),
            ],
        )

        if not path:
            return

        try:
            vertices, faces = load_obj_file(path)
        except (OSError, UnicodeError, ValueError) as error:
            messagebox.showerror("OBJ loading failed", str(error), parent=self.root)
            return

        # Update state only after successful loading.
        self.indexed_face = IndexedFace(vertices, faces)

        self.filename.set(Path(path).name)
        self.vertex_count.set(f"Vertices (v): {len(vertices)}")
        self.face_count.set(f"Faces (f): {len(faces)}")

        self.canvas.delete("placeholder")

        self.draw_objects()

    # ------------------------------------------------------------------
    # Drawing (your code)
    # ------------------------------------------------------------------
    def transform_points(self) -> List[Tuple[Vec4, Vec4, Vec4, Vec4, Vec4]]:  # p1,p2,p3, normal, center
        vertices = self.indexed_face.get_vertices() # type: ignore

        points = []

        for face in self.indexed_face.get_faces(): # type: ignore , its none only because its loaded 
            p1: Vec4 = vertices[face[0]]
            p2: Vec4 = vertices[face[1]]
            p3: Vec4 = vertices[face[2]]

            p1 = VIEW_TRANSFORMATION * OBJECT_TRANSFORMATION * p1  # type: ignore
            p2 = VIEW_TRANSFORMATION * OBJECT_TRANSFORMATION * p2  # type: ignore
            p3 = VIEW_TRANSFORMATION * OBJECT_TRANSFORMATION * p3  # type: ignore

            # back-face culling
            N = normalize(cross_product(p2 - p1, p3 - p1))
            V = Vec4(0, 0, 1, 0)  # w=0 since its a vector

            if dot_product(N, V) <= 0:  # we only draw a face iff dot_product(N,V) > 0
                continue

            center = Vec4(
                (p1[0] + p2[0] + p3[0]) / 3,
                (p1[1] + p2[1] + p3[1]) / 3,
                (p1[2] + p2[2] + p3[2]) / 3,
                1,
            )

            p1 = PROJECTION_TRANSFORMATION * p1  # type: ignore
            p2 = PROJECTION_TRANSFORMATION * p2  # type: ignore
            p3 = PROJECTION_TRANSFORMATION * p3  # type: ignore

            points.append(tuple([p1, p2, p3, N, center]))

        return points

    def draw_objects(self):
        global WIREFRAME

        if self.indexed_face is None:  # nothing loaded yet
            return

        self.canvas.delete("model")

        points = self.transform_points()

        for polygon in points:
            p1, p2, p3, _, _ = polygon

            if WIREFRAME:
                self.draw_line(p1, p2)
                self.draw_line(p2, p3)
                self.draw_line(p3, p1)
            else:  # draw polygons
                self.draw_triangle(polygon)

    def draw_line(self, p1: Vec4, p2: Vec4):
        global  LINE_WIDTH

        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]

        self.canvas.create_line(x1, y1, x2, y2, fill=rgb_to_hex(self.material.color), width=LINE_WIDTH, tag="model")  # type: ignore

    def draw_triangle(self, polygon: Tuple[Vec4, Vec4, Vec4, Vec4, Vec4]):
        """
        points: p1,p2,p3, normal, center
        """
        global VIEW_DIRECTION

        x1, y1 = polygon[0][0], polygon[0][1]
        x2, y2 = polygon[1][0], polygon[1][1]
        x3, y3 = polygon[2][0], polygon[2][1]
        normal = polygon[3]
        center = polygon[4]

        color = self.shader_model.shade(
            point=center,
            normal=normal,
            angle_of_viewer=VIEW_DIRECTION,
            light_source=self.light,
            material=self.material,
        )

        self.canvas.create_polygon(
            x1, y1, x2, y2, x3, y3,
            outline="",
            fill=rgb_to_hex(color),
            width=1,
            tags="model",
        )

    # ------------------------------------------------------------------
    # Transformations (still my code)
    # ------------------------------------------------------------------
    def translate(self):
        tx, ty, tz = float(self.tx.get()), float(self.ty.get()), float(self.tz.get())
        self.apply_matrix(get_translation_matrix(tx, ty, tz))

    def rotate(self):
        rx, ry, rz = float(self.rx.get()), float(self.ry.get()), float(self.rz.get())
        self.apply_matrix(combine_transformation_matrices([
            get_rotation_x_axis_matrix(rx),
            get_rotation_y_axis_matrix(ry),
            get_rotation_z_axis_matrix(rz),
        ]))

    def scale_model(self):
        factor = float(self.scale.get())
        self.apply_matrix(get_scaling_matrix(factor, factor, factor))

    def apply_matrix(self, matrix: Mat4):
        global OBJECT_TRANSFORMATION
        OBJECT_TRANSFORMATION = matrix * OBJECT_TRANSFORMATION
        self.draw_objects()

    def reset(self):
        global OBJECT_TRANSFORMATION
        for entry, value in (
            (self.tx, "0"), (self.ty, "0"), (self.tz, "0"),
            (self.rx, "0"), (self.ry, "0"), (self.rz, "0"),
            (self.scale, "1"),
        ):
            entry.delete(0, tk.END)
            entry.insert(0, value)

        OBJECT_TRANSFORMATION = get_identity_matrix()
        self.draw_objects()