import tkinter as tk

from src import states


class Box:
    size = 12

    def __init__(self, i:int, j:int):
        self.i = i
        self.j = j
        self.iid = None
        self.state = states.EMPTY

    def set_state(self, new_state, canvas:tk.Canvas):
        """
        Sets the state of the box.
        """

        self.state = new_state
        self.update(canvas)

    def create(self, canvas:tk.Canvas):
        """
        Creates the box in the grid.
        """

        self.iid = canvas.create_rectangle(
            2 + self.j * self.size,
            2 + self.i * self.size,
            2 + (self.j + 1) * self.size,
            2 + (self.i + 1) * self.size,
            fill="#e0e0f0",
            outline="#a0a0b0"
        )

    def update(self, canvas:tk.Canvas):
        """
        Updates the box in the grid.
        """

        fill = {
            states.EMPTY: "#e0e0f0",
            states.SNAKE: "green",
            states.FOOD: "red"
        }.get(self.state)

        canvas.itemconfigure(self.iid, fill=fill)
