from src.zpgso_graphics_project.modules.gui import RendererGUI
import tkinter as tk

from src.zpgso_graphics_project.modules.vec4 import Vec4, cross_product

if __name__ == "__main__":
    print(cross_product(Vec4(1,0,0,0), Vec4(0,1,0,0)))   # must be (0, 0, 1)
    root = tk.Tk()
    app = RendererGUI(root)
    root.mainloop()
