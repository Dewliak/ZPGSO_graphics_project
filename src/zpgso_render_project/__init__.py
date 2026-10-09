#from modules.gui import RendererGUI
import tkinter as tk
from src.zpgso_render_project.modules.gui import RendererGUI
def main() -> None:
    root = tk.Tk()
    app = RendererGUI(root)
    root.mainloop()