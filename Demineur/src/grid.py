import tkinter as tk

from src.box import Box


class Grid:
    def __init__(self, canvas:tk.Canvas):
        self.canvas = canvas
        self.grid = list()
        self.size = [0, 0]
        self.box_size = 16
        self.box_pad = 1

        self.n_bombs = 0

    def init(self, size:list):
        """
        Initializes and resets the grid.

        Args:
            size (list): the new size (row, col)
        """

        # Set new size
        self.size = list(size)
        w = self.size[0] * self.box_size
        h = self.size[1] * self.box_size
        self.canvas.configure(width=w, height=h)

        # Remove all elements in the grid
        self.grid.clear()
        self.n_bombs = 0

        # Fill the grid
        for i in range(size[0]):
            line = list()
            for j in range(size[1]):
                x = j * self.box_size
                y = i * self.box_size
                iid = self.canvas.create_rectangle(
                    1 + x + self.box_pad,
                    1 + y + self.box_pad,
                    x + self.box_size,
                    y + self.box_size,
                    fill="#e0e0f0",
                    outline="#a0a0b0"
                )
                line.append(Box(i, j, iid))
            self.grid.append(line)

    def set_bomb(self, i, j):
        """
        Sets a bomb at the given position.
        """

        self.grid[i][j].set_bomb()
        self.n_bombs += 1

    def process_values(self):
        """
        Porcesses the grid to set the values.
        """

        # For all the boxes in the grid
        for box in self.list_boxes():
            # # If it's not a bomb
            n = 0
            if not box.is_bomb():
                neighbours = box.get_pos_neighbours()
                for i, j in neighbours:
                    if i >= 0 and i < self.size[0] and \
                       j >= 0 and j < self.size[1]:
                        n += self.grid[i][j].is_bomb()
                box.set_value(n)

    def clicked(self, x, y):
        """
        x and y are real positions.
        Processes the boxes when ea box is clicked.
        """

        # Get clicked box
        i = y // self.box_size
        j = x // self.box_size
        box = self.grid[i][j]

        # If it's a flag, do nothing
        if box.flag:
            return

        # Show the bomb
        if box.is_bomb():
            self.show_box(box)
            return -1
        # Show the value
        else:
            # If it's not 0
            if box.value != 0:
                self.show_box(box)
            # If it's 0
            else:
                zone_try = set()
                zone_try.add((i, j))

                while zone_try:
                    i, j = coord = zone_try.pop()
                    box = self.grid[i][j]
                    if box.reveal:
                        continue

                    self.show_box(box)

                    ok = str()

                    # Reveal boxes with value 0
                    # North
                    if i > 0:
                        ok += "n"
                        if self.grid[i-1][j].value == 0:
                            zone_try.add((i-1, j))
                    # South
                    if i < self.size[0] - 1:
                        ok += "s"
                        if self.grid[i+1][j].value == 0:
                            zone_try.add((i+1, j))
                    # West
                    if j > 0:
                        ok += "w"
                        if self.grid[i][j-1].value == 0:
                            zone_try.add((i, j-1))
                    # East
                    if j < self.size[1]-1:
                        ok += "e"
                        if self.grid[i][j+1].value == 0:
                            zone_try.add((i, j+1))

                    # Reveal boxes with value > 0
                    # North
                    if "n" in ok and \
                       self.grid[i-1][j].value > 0:
                        self.show_box(self.grid[i-1][j])
                    # North east
                    if "n" in ok and "e" in ok and \
                       self.grid[i-1][j+1].value > 0:
                        self.show_box(self.grid[i-1][j+1])
                    # East
                    if "e" in ok and \
                       self.grid[i][j+1].value > 0:
                        self.show_box(self.grid[i][j+1])
                    # South east
                    if "s" in ok and "e" in ok and \
                       self.grid[i+1][j+1].value > 0:
                        self.show_box(self.grid[i+1][j+1])
                    # South
                    if "s" in ok and \
                       self.grid[i+1][j].value > 0:
                        self.show_box(self.grid[i+1][j])
                    # South west
                    if "s" in ok and "w" in ok and \
                       self.grid[i+1][j-1].value > 0:
                        self.show_box(self.grid[i+1][j-1])
                    # West
                    if "w" in ok and \
                       self.grid[i][j-1].value > 0:
                        self.show_box(self.grid[i][j-1])
                    # North west
                    if "n" in ok and "w" in ok and \
                       self.grid[i-1][j-1].value > 0:
                        self.show_box(self.grid[i-1][j-1])

        # Check if win the game

    def flag(self, x, y):
        """
        Manages the flag at given positon
        """

        # Get box
        i = y // self.box_size
        j = x // self.box_size
        box = self.grid[i][j]

        # Do not flag revealed boxes
        if box.reveal:
            return

        if box.flag == "":
            self.show_flag(box)
        elif box.flag == "#":
            self.show_interrogation(box)
        elif box.flag == "?":
            self.hide_flag(box)

    def show_box(self, box):
        """
        Shows a box on the canvas.
        """

        box.reveal = True
        if box.is_bomb():
            self.canvas.itemconfigure(box.iid, fill="red", outline="white")
        elif box.value == 0:
            self.canvas.itemconfigure(box.iid, fill="white", outline="white")
        else:
            self.canvas.itemconfigure(box.iid, fill="white", outline="white")
            self.canvas.create_text(
                1 + box.j * self.box_size + self.box_size // 2,
                1 + box.i * self.box_size + self.box_size // 2,
                text=str(box.value)
            )

        self.hide_flag(box)

    def show_flag(self, box):
        """
        Show the flag
        """

        box.flag = "#"
        self.canvas.delete(box.flag_iid)
        box.flag_iid = self.canvas.create_text(
            1 + box.j * self.box_size + self.box_size // 2,
            1 + box.i * self.box_size + self.box_size // 2,
            text="#",
            fill="#a00000",
            font=("Segoe UI", 9, "bold")
        )

    def show_interrogation(self, box):
        """
        Show the interrogation symbol
        """

        box.flag = "?"
        self.canvas.delete(box.flag_iid)
        box.flag_iid = self.canvas.create_text(
            box.j * self.box_size + self.box_size // 2 + self.box_pad,
            box.i * self.box_size + self.box_size // 2 + self.box_pad,
            text="?",
            fill="#00a000",
            font=("Segoe UI", 9, "bold")
        )

    def hide_flag(self, box):
        """
        Hides the flag
        """

        box.flag = ""
        self.canvas.delete(box.flag_iid)
        box.flag_iid = None

    def has_win(self):
        """
        Checks if win the game
        """

        n = 0
        for box in self.list_boxes():
            if not box.reveal:
                n += 1

        # Win if there only the bombs are hidden
        return n == self.n_bombs

    # Tools

    def list_boxes(self):
        """
        Returns a generator that lists all the boxes in the grid.
        """

        for line in self.grid:
            for box in line:
                yield box
