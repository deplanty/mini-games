

class Box:
    def __init__(self, i, j, iid):
        self.i = i
        self.j = j
        self.iid = iid
        self.value = 0
        self.reveal = False
        self.flag = ""
        self.flag_iid = None

    def set_value(self, value):
        self.value = value

    def set_bomb(self):
        self.value = -1

    def is_bomb(self):
        return self.value == -1

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
