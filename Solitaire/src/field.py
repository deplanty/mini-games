import tkinter as tk

from src import tags


class Field:
    def __init__(self, canvas:tk.Canvas):

        self.canvas = canvas
        self.size = 7
        self.pixel_box = 32
        self.grid = list()

        wh = self.size * self.pixel_box + 1
        self.canvas.configure(width=wh, height=wh, background="black")

    def init(self):
        """
        Initializes a new field.
        """

        # Remove all elements in the field
        for line in self.grid:
            self.canvas.delete(*line)
        self.grid.clear()

        # Fill the field
        for i in range(self.size):
            line = list()
            for j in range(self.size):
                iid = self.canvas.create_rectangle(
                    i * self.pixel_box + 2,
                    j * self.pixel_box + 2,
                    (i+1) * self.pixel_box + 2,
                    (j+1) * self.pixel_box + 2,
                    fill="#5080b0",
                    outline="white",
                    tag=(i, j, tags.PAWN)
                )
                line.append(iid)
            self.grid.append(line)

        # Remove the corners
        for i in [0, 1, 5, 6]:
            for j in [0, 1, 5, 6]:
                self.canvas.delete(self.grid[i][j])
                self.grid[i][j] = None

    def toggle(self, iid):
        """
        Removes or places a pawn from its iid.
        """

        i, j, tag = self.get_info(iid)

        # Place a pawn
        if tag in (tags.PAWN, tags.PAWN_SELECTED):
            self.canvas.itemconfigure(iid, fill="black", tag=(i, j, tags.EMPTY))
        # Remove a pawn
        elif tag in (tags.EMPTY, tags.EMPTY_TARGET):
            self.canvas.itemconfigure(iid, fill="#5080b0", tag=(i, j, tags.PAWN))

    def show_movable_pawns(self):
        """
        Shows the movable pawns and set its tag.
        """

        # Reset the tags and the colors
        for item in self.gen_boxes():
            i, j, tag = self.get_info(item)
            if tag == tags.EMPTY_TARGET:
                self.canvas.itemconfigure(item, fill="black", tag=(i, j, tags.EMPTY))
            elif tag in (tags.PAWN_SELECTED, tags.PAWN_MOVABLE):
                self.canvas.itemconfigure(item, fill="#5080b0", tag=(i, j, tags.PAWN))

        # Process the items
        for iid in self.gen_boxes():
            i, j, tag = self.get_info(iid)
            # If the box is empty
            if tag == tags.EMPTY:
                moves = self.get_movement_positions(i, j)
                # Show all the movable pawns
                for item in moves:
                    ii, jj, item_tag = self.get_info(item)
                    if item_tag == tags.PAWN:
                        self.canvas.itemconfigure(item, fill="#b0a020", tag=(ii, jj, tags.PAWN_MOVABLE))

    def show_target_box(self, iid):
        """
        Shows the target boxes from a pawn and set its tag.
        """

        # Reset the tags and the colors
        for item in self.gen_boxes():
            i, j, tag = self.get_info(item)
            if tag in (tags.PAWN_MOVABLE, tags.PAWN_SELECTED):
                self.canvas.itemconfigure(item, fill="#5080b0", tag=(i, j, tags.PAWN))

        # Process pawn
        i, j, tag = self.get_info(iid)
        self.canvas.itemconfigure(iid, fill="#b06020", tag=(i, j, tags.PAWN_SELECTED))
        # If the box is empty
        if tag == tags.PAWN:
            moves = self.get_movement_positions(i, j)
            # Show all the movable pawns
            for item in moves:
                ii, jj, item_tag = self.get_info(item)
                if item_tag == tags.EMPTY:
                    self.canvas.itemconfigure(item, fill="#b0a020", tag=(ii, jj, tags.EMPTY_TARGET))

    # Tools

    def get_info(self, iid):
        """
        Returns the tags of an item.
        """

        tag = self.canvas.itemcget(iid, "tag").split()
        return int(tag[0]), int(tag[1]), int(tag[2])

    def get_pos(self, iid):
        """
        Returns the position of the item.
        """

        tag = self.canvas.itemcget(iid, "tag").split()
        return int(tag[0]), int(tag[1])

    def get_tag(self, iid):
        """
        Returns the tag of the item.
        """

        tag = self.canvas.itemcget(iid, "tag").split()
        return int(tag[2])

    def get_grid_pos(self, x, y):
        """
        Returns the grid position (i, j) from mouse position (x, y)
        """

        i = x // self.pixel_box
        j = y // self.pixel_box
        return i, j

    def get(self, x, y):
        """
        Returns the element at the given position.
        It can be None or the item iid.
        """

        i, j = self.get_grid_pos(x, y)
        return self.grid[i][j]

    def get_movement_positions(self, i, j):
        """
        Returns the item iid of the boxes if a movement is made.
        """

        items = list()
        # North
        if i - 2 >= 0:
            target = self.grid[i - 2][j]
            between = self.grid[i - 1][j]
            # If the target exists and the box in between is a pawn
            if target and self.get_tag(between) in (tags.PAWN, tags.PAWN_SELECTED, tags.PAWN_MOVABLE):
                items.append(target)
        # East
        if j + 2 < self.size:
            target = self.grid[i][j + 2]
            between = self.grid[i][j + 1]
            if target and self.get_tag(between) in (tags.PAWN, tags.PAWN_SELECTED, tags.PAWN_MOVABLE):
                items.append(target)
        # South
        if i + 2 < self.size:
            target = self.grid[i + 2][j]
            between = self.grid[i + 1][j]
            if target and self.get_tag(between) in (tags.PAWN, tags.PAWN_SELECTED, tags.PAWN_MOVABLE):
                items.append(target)
        # West
        if j - 2 >= 0:
            target = self.grid[i][j - 2]
            between = self.grid[i][j - 1]
            if target and self.get_tag(between) in (tags.PAWN, tags.PAWN_SELECTED, tags.PAWN_MOVABLE):
                items.append(target)

        return items

    def box_is(self, iid, tag):
        """
        Checks if a box is a certain tag.
        """

        _, _, item_tag = self.get_info(iid)
        return item_tag == tag

    def gen_boxes(self):
        """
        Returns the boxes iid.
        Generator.
        """

        for line in self.grid:
            for box in line:
                if box is not None:
                    yield box
