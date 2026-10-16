import tkinter as tk

from src.zpgso_graphics_project.modules.gui import RendererGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = RendererGUI(root)
    root.mainloop()
