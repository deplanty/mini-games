import tkinter as tk

from src.box import Box


class Grid:
    def __init__(self):

        self.grid = list()
        self.size = list()

    def load(self, file:str):

        self.grid.clear()

        with open(file) as fid:
            for line in fid:
                row = list()
                for element in line.rstrip().split():
                    row.append(Box(element))
                self.grid.append(row)

        i = len(self.grid)
        j = len(self.grid[0])
        self.size = [i, j]

    def hint_line(self, line:list):
        """
        Return the hint for a line
        """

        hint = list()
        n = 0
        for box in line:
            # If it's a blanck
            if box.s == ".":
                hint.append(n)
                n = 0
            # if it's a value:
            elif box.s == "#":
                n += 1
        # Add last value
        hint.append(n)

        # Remove all the 0
        while 0 in hint:
            hint.remove(0)

        return hint

    def hint_row(self, n_row:int):
        """
        Returns the hint for the given row.
        """

        row = self.grid[n_row]
        return self.hint_line(row)

    def hint_column(self, n_column:int):
        """
        Returns the hint for the given column.
        """

        col = [self.grid[i][n_column] for i in range(self.size[0])]
        return self.hint_line(col)

    def gen_boxes(self) -> Box:
        """
        Returns all the boxes in the grid.
        Generator.
        """

        for row in self.grid:
            for element in row:
                yield element

    # Magics

    def __getitem__(self, row):
        return self.grid[row]
