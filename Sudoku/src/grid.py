import tkinter as tk

from src.box import Box


class Grid:
    def __init__(self, canvas:tk.Canvas):
        self.canvas = canvas
        self.grid = list()
        self.size = 9
        self.box_size = 32

        wh = self.size * self.box_size + 2
        self.canvas.configure(width=wh, height=wh)

    def init(self, file:str):
        """
        Initializes and resets the grid.
        Loads a grid from a file.
        """


        # Remove all elements in the grid
        self.grid.clear()

        # Load the new grid
        with open(file) as fid:
            grid = list()
            for line in fid:
                grid.append(line.rstrip().split(","))

        # Fill the grid
        for i in range(self.size):
            line = list()
            for j in range(self.size):
                box = Box(i, j)
                box.value = grid[i][j]
                box.fixed = grid[i][j] != ""
                font = "bold" if box.fixed else "normal"
                box.box_iid = self.canvas.create_rectangle(
                    2 + j * self.box_size,
                    2 + i * self.box_size,
                    2 + (j + 1) * self.box_size,
                    2 + (i + 1) * self.box_size,
                    fill="#e0e0f0",
                    outline="#a0a0b0"
                )
                box.value_iid = self.canvas.create_text(
                    2 + (j + 0.5) * self.box_size,
                    2 + (i + 0.5) * self.box_size,
                    text=grid[i][j],
                    font=("Calibri", 12, font)
                )
                line.append(box)
            self.grid.append(line)

        # Creates big lines
        for i in range(4):
            self.canvas.create_line(
                2,
                2 + 3 * i * self.box_size,
                2 + self.size * self.box_size,
                2 + 3 * i * self.box_size,
                width=3
            )

        for j in range(4):
            self.canvas.create_line(
                2 + 3 * j * self.box_size,
                2,
                2 + 3 * j * self.box_size,
                2 + self.size * self.box_size,
                width=3
            )

    def set_value(self, i, j, value):
        """
        Sets the value at the given grid position.
        """

        box:Box = self.grid[i][j]
        box.value = value
        self.canvas.itemconfigure(box.value_iid, text=value)

    # Checking

    def check_grid(self):
        """
        Checks all the grid
        """

        is_correct = False
        for i in range(self.size):
            for j in range(self.size):
                is_correct = self.check_box(i, j)

        return is_correct

    def check_box(self, i, j):
        """
        Checks if the box is correct.
        """

        box = self.grid[i][j]
        if box.value == "":
            self.canvas.itemconfigure(box.box_iid, fill="#e0e0f0")
            return False

        if self.get_row(i).count(box.value) > 1 or \
           self.get_column(j).count(box.value) > 1 or \
           self.get_square(i, j).count(box.value) > 1:
            self.canvas.itemconfigure(box.box_iid, fill="#e09080")
            return False
        else:
            self.canvas.itemconfigure(box.box_iid, fill="#e0e0f0")
            return True

    # Tools

    def get_position(self, x, y):
        """
        Returns the grid position from pixel position.
        """

        i = (y - 2) // self.box_size
        j = (x - 2) // self.box_size

        return i, j

    def get_row(self, i):
        """
        Returns the values of the row.
        """

        row = [box.value for box in self.grid[i]]
        return row

    def get_column(self, j):
        """
        Returns the values of the column.
        """

        column = [self.grid[i][j].value for i in range(self.size)]
        return column

    def get_square(self, i, j):
        """
        Returns the values of the square from a box position.
        """

        i_sqr = i // 3
        j_sqr = j // 3

        square = list()
        for i in range(3):
            for j in range(3):
                square.append(self.grid[i + i_sqr*3][j + j_sqr*3].value)

        return square

    def gen_boxes(self):
        """
        Returns all the boxes in the grid.
        Generator.
        """

        for line in self.grid:
            for box in line:
                yield box

    # Magics

    def __getitem__(self, index):
        return self.grid[index]
