import tkinter as tk
from tkinter import ttk


class UI_Main(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.set_ui()

    # UI

    def set_ui(self):
        """
        Sets the elements in the frame.
        """

        # Top frame
        self.frame_top = ttk.Frame(self)
        self.frame_top.pack(fill="x")

        self.button = ttk.Button(self.frame_top, text="Continuer")
        self.button.pack(side="left", padx=5, pady=2)
        self.label = ttk.Label(self.frame_top, text="Placer des étoiles")
        self.label.pack(side="left", padx=5, pady=2)

        # Canvas
        self.canvas = tk.Canvas(self, background="black")
        self.canvas.pack(fill="both", expand=True)
