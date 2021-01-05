import tkinter as tk

from src.box import Box


class Grid:
    def __init__(self, canvas:tk.Canvas):
        self.canvas = canvas
        self.grid = list()
        self.grid_size = list()
        self.size = [0, 0]
        self.box_size = 12

    def init(self, size:list):
        """
        Initializes and resets the grid.

        Args:
            size (list): the new size (row, col)
        """

        # Set new size
        self.size = list(size)
        w = self.size[1] * self.box_size + 1
        h = self.size[0] * self.box_size + 1
        self.canvas.configure(width=w, height=h, background="#ff0000")
        self.grid_size = (w, h)

        # Remove all elements in the grid
        for box in self.gen_boxes():
            self.canvas.delete(box.iid)
        self.grid.clear()

        # Fill the grid
        for i in range(size[0]):
            line = list()
            for j in range(size[1]):
                x = j * self.box_size + 2
                y = i * self.box_size + 2
                iid = self.canvas.create_rectangle(
                    x,
                    y,
                    x + self.box_size,
                    y + self.box_size,
                    fill="black",
                    outline="#404545"
                )
                line.append(Box(i, j, iid))
            self.grid.append(line)

    def born(self, i, j):
        """
        Born at the given position.
        """

        box = self.grid[i][j]
        box.born()

    def kill(self, i, j):
        """
        Kills at the given position.
        """

        box = self.grid[i][j]
        box.kill()

    def toggle(self, i, j):
        """
        Kills a living box or give birth to a dead one.
        """

        box = self.grid[i][j]
        if box.living:
            box.kill()
        else:
            box.born()
        self.apply(box)

    def apply(self, box=None):
        """
        Applies all the modifications.
        """

        if box is None:
            for box in self.gen_boxes():
                box.apply()
                if box.living:
                    self.canvas.itemconfigure(box.iid, fill="white")
                else:
                    self.canvas.itemconfigure(box.iid, fill="black")
        else:
            box.apply()
            if box.living:
                self.canvas.itemconfigure(box.iid, fill="white")
            else:
                self.canvas.itemconfigure(box.iid, fill="black")

    def process_box(self, box:Box):
        """
        Processes the box to determine its new state.
        """

        # Get the number of living boxes around this box
        n = 0
        for i, j in box.get_pos_neighbours():
            # Noth west
            if i >= 0 and j >= 0 and \
               i < self.size[0] and j < self.size[1]:
                n += self.grid[i][j].living

        # Process the rules
        if not box.living and n == 3:
            box.born()
        elif box.living and (n < 2 or n > 3):
            box.kill()

    # Tools

    def gen_boxes(self):
        """
        Returns a generator that lists all the boxes in the grid.
        """

        for line in self.grid:
            for box in line:
                yield box
