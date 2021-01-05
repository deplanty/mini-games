class Box:
    def __init__(self, i, j, iid):
        self.i = i
        self.j = j
        self.iid = iid
        self.living = False
        self.pending = False

    def born(self):
        self.pending = True

    def kill(self):
        self.pending = False

    def apply(self):
        self.living = self.pending

    def get_pos_neighbours(self):
        """
        Returns the position of all the neighbours boxes.
        Generator.
        """

        for i in range(-1, 2):
            for j in range(-1, 2):
                # Do not take self
                if i == 0 and j == 0:
                    continue
                ii = self.i + i
                jj = self.j + j
                yield ii, jj
