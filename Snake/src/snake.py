from src import states


class Snake:
    def __init__(self, boundaries:list):
        self.body = list()
        self.direction = int()
        self.bounds = boundaries

        self.init()

    def init(self):
        self.direction = states.WEST

    def move(self):
        """
        Adds the new head and removes the tail.

        Returns:
            list: new head (i, j)
            list: ols tail (i, j)
        """

        old_head = self.body[0]
        i_head, j_head = [
            old_head[0] + self.direction[0],
            old_head[1] + self.direction[1],
        ]

        if i_head < 0:
            i_head = self.bounds[1] - 1
        elif i_head >= self.bounds[1]:
            i_head = 0

        if j_head < 0:
            j_head = self.bounds[0] - 1
        elif j_head >= self.bounds[0]:
            j_head = 0

        self.body.insert(0, (i_head, j_head))

        i_tail, j_tail = self.body.pop(-1)

        return (i_head, j_head), (i_tail, j_tail)

    def eat_tail(self):
        """
        Returns if the snake eats its tail.
        """

        body = set(self.body)
        return len(body) < len(self.body)

    # Magics

    def __getitem__(self, index):
        return self.body[index]
