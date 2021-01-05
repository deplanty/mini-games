import tkinter as tk

from src.box import Box
from src.grid import Grid
from src import states


class View:
    def __init__(self, canvas:tk.Canvas):
        self.canvas = canvas
        self.box_size = 20
        self.grid = Grid()
        self.hint_items = list()

    def init(self, file:str):

        # Clear previous grid
        self.canvas.delete(*self.hint_items)
        self.hint_items.clear()

        for box in self.grid.gen_boxes():
            self.canvas.delete(box.iid)

        # Init the grid
        self.grid.load(file)

        # Get hints
        hints_row = list()
        for i in range(self.grid.size[0]):
            hints_row.append(self.grid.hint_row(i))
        hints_col = list()
        for j in range(self.grid.size[1]):
            hints_col.append(self.grid.hint_column(j))

        # Max hint size
        self.max_hint_row = max(map(len, hints_row))
        self.max_hint_col = max(map(len, hints_col))

        # Set canvas size
        self.grid_start = [
            self.max_hint_col * self.box_size,
            self.max_hint_row * self.box_size
        ]
        w = 1 + self.grid_start[1] + self.grid.size[1] * self.box_size
        h = 1 + self.grid_start[0] + self.grid.size[0] * self.box_size
        self.canvas.configure(width=w, height=h)

        # Set the grid
        for i in range(self.grid.size[0]):
            for j in range(self.grid.size[1]):
                iid = self.canvas.create_rectangle(
                    2 + self.grid_start[1] + j * self.box_size,
                    2 + self.grid_start[0] + i * self.box_size,
                    self.grid_start[1] + (j + 1) * self.box_size + 2,
                    self.grid_start[0] + (i + 1) * self.box_size + 2,
                    fill="white",
                    outline="gray"
                )
                self.grid[i][j].iid = iid

        # Set the hints next to the grid
        for i, hints in enumerate(hints_row):
            for j, hint in enumerate(hints):
                iid = self.canvas.create_text(
                    (j + 0.5) * self.box_size,
                    self.grid_start[0] + (i + 0.5) * self.box_size,
                    text=hint
                )
                self.hint_items.append(iid)

        for j, hints in enumerate(hints_col):
            for i, hint in enumerate(hints):
                iid = self.canvas.create_text(
                    self.grid_start[1] + (j + 0.5) * self.box_size,
                    (i + 0.5) * self.box_size,
                    text=hint
                )
                self.hint_items.append(iid)

    def toggle(self, x, y):
        """
        Toggles the box at the given position
        """

        i, j = self.get_grid_pos(x, y)

        if i >= 0 and j >= 0:
            box:Box = self.grid[i][j]
            if box.state == states.HIDDEN:
                self.show_box(i, j)
            elif box.state == states.REVEALED:
                self.hide_box(i, j)

    def show_box(self, i, j):
        """
        Shows the box at given coordinates.
        """

        box:Box = self.grid[i][j]
        box.state = states.REVEALED
        self.canvas.itemconfigure(box.iid, fill="black")

    def hide_box(self, i, j):
        """
        Hides the box at given coordinates.
        """

        box:Box = self.grid[i][j]
        box.state = states.HIDDEN
        self.canvas.itemconfigure(box.iid, fill="white")

    def check_win(self):
        """
        Checks if the player has won the game.
        """

        # For all the boxes
        for box in self.grid.gen_boxes():
            # If at least one box is incorrect
            if (box.s == "#" and box.state != states.REVEALED) or \
               (box.s == "." and box.state != states.HIDDEN):
                # The game continue
                return False
        # If all the boxes are correct
        return True


    # Tools

    def get_grid_pos(self, x, y):
        """
        Returns the grid position from real pixel position.
        """

        i = (y - self.grid_start[0]) // self.box_size
        j = (x - self.grid_start[1]) // self.box_size

        return i, j
