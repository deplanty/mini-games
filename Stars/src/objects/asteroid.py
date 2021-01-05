import tkinter as tk

import src.constants as cst
from src import tools


class Asteroid:
    def __init__(self, canvas:tk.Canvas, x:int, y:int, radius:int):
        # Radius
        self.r = radius
        # Position
        self.x = x
        self.y = y
        # Velocity
        self.v_x = 0
        self.v_y = 0
        # Acceleration
        self.a_x = 0
        self.a_y = 0

        self.iid = None
        self.iid_arrow = None
        self.canvas = canvas

    def init(self):
        """
        Initializes the asteroid and draws it a first tome
        """

        self.iid_arrow = self.canvas.create_line(
            self.x,
            self.y,
            self.x + self.v_x * 10,
            self.y + self.v_y * 10,
            arrow="last",
            fill="red"
        )

        self.iid = self.canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill="white",
            outline="lightgrey"
        )

    def move(self, dt:float, stars:list):
        """
        Moves the asteroid according to the nearest star.
        """

        v_x = 0
        v_y = 0
        for star in stars:
            r_x, r_y = tools.vect([self.x, self.y], [star.x, star.y])
            r = tools.norm([r_x, r_y])

            g = (cst.G * star.mass * dt) / (r**3)
            v_x += g * r_x
            v_y += g * r_y

        self.v_x = v_x + self.v_x
        self.v_y = v_y + self.v_y

        self.x += self.v_x
        self.y += self.v_y
        self.canvas.move(self.iid, self.v_x, self.v_y)

        self.canvas.coords(
            self.iid_arrow,
            self.x,
            self.y,
            self.x + self.v_x * 10,
            self.y + self.v_y * 10
        )

    def update_draw(self):
        """
        Updates the drawing of the asteroid
        """

        self.canvas.coords(
            self.iid_arrow,
            self.x,
            self.y,
            self.x + self.v_x * 10,
            self.y + self.v_y * 10
        )

        self.canvas.coords(
            self.iid,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )
