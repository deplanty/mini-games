import tkinter as tk


class Star:
    def __init__(self, canvas:tk.Canvas, x:int, y:int, radius:int, mass:int):
        self.r = radius
        self.x = x
        self.y = y

        self.mass = mass

        self.iid = None
        self.canvas = canvas

    def init(self):
        """
        Initalizes the star and draw it
        """

        self.iid = self.canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill="yellow"
        )
