import random
import tkinter as tk

from src.box import Box
from src.snake import Snake
from src import states


class Game:
    def __init__(self, canvas:tk.Canvas):
        self.canvas = canvas
        self.grid = list()
        self.size = [24, 24]
        self.snake = Snake(self.size)
        self.score = 0

        w = self.size[0] * Box.size + 1
        h = self.size[1] * Box.size + 1
        self.canvas.configure(width=w, height=h)

    def init(self):
        """
        Initializes and resets the grid.
        Loads a grid from a file.
        """

        # Remove all elements in the grid
        self.grid.clear()

        # Fill the grid
        for i in range(self.size[1]):
            line = list()
            for j in range(self.size[0]):
                box = Box(i, j)
                box.create(self.canvas)
                line.append(box)
            self.grid.append(line)

        # Snake
        self.snake.init()
        i_mid = self.size[1] // 2
        j_mid = self.size[0] // 2
        self.snake.body = [(i_mid, j_mid), (i_mid, j_mid+1), (i_mid, j_mid+2)]
        for i, j in self.snake:
            self.grid[i][j].set_state(states.SNAKE, self.canvas)

        self.score = 0
        self.spawn_food()

    # Snake

    def move(self):
        """
        Moves the snake on the grid.
        """

        new_head, old_tail = self.snake.move()
        box = self.grid[new_head[0]][new_head[1]]

        # If there is food, do not remove the tail
        if box.state == states.FOOD:
            self.snake.body.append(old_tail)
            self.score += 1
            self.spawn_food()
        # Remove the tail
        else:
            i, j = old_tail
            self.grid[i][j].set_state(states.EMPTY, self.canvas)

        # Add the head
        box.set_state(states.SNAKE, self.canvas)

        return self.snake.eat_tail()

    # Food

    def spawn_food(self):
        """
        Adds a food in the grid.
        """

        boxes = [box for box in self.gen_boxes() if box.state == states.EMPTY]
        box = random.choice(boxes)
        box.set_state(states.FOOD, self.canvas)

    # Tools

    def gen_boxes(self) -> Box:
        """
        Lists all the boxes in the grid.
        Generator.
        """

        for i in range(self.size[1]):
            for j in range(self.size[0]):
                yield self.grid[i][j]

    # Magics

    def __getitem__(self, index):
        return self.grid[index]
