import tkinter as tk

from src.game import Game
from src import states


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.iid_after = None
        self.state = states.PAUSE

        self.withdraw()
        self.title("Snake")
        self.set_ui()
        self.set_events()
        self.init_new_game()
        self.resizable(False, False)
        self.deiconify()

    # UI

    def set_ui(self):
        """
        Sets elements in the UI.
        """

        self.label_score = tk.Label(self, width=5, height=2, justify="center")
        self.label_score.pack(fill="x", padx=5, pady=5)

        self.canvas = tk.Canvas(self)
        self.canvas.pack()

        self.game = Game(self.canvas)

    def set_events(self):
        """
        Sets the events in the UI.
        """

        self.bind("<Right>", self.event_arrow_right)
        self.bind("<Left>", self.event_arrow_left)
        self.bind("<Up>", self.event_arrow_up)
        self.bind("<Down>", self.event_arrow_down)
        self.bind("<space>", self.event_space)

    # Game methods

    def init_new_game(self):
        """
        Initializes a new game.
        """

        self.game.init()
        self.label_score.configure(text="Appuyer sur Espace pour commencer")
        self.state = states.PAUSE

    def loop(self):
        """
        Game loop.
        """

        lose = self.game.move()
        if not lose:
            self.iid_after = self.after(100, self.loop)
            self.label_score.configure(text=self.game.score)
        else:
            self.state = states.END
            self.label_score.configure(text=f"Score final : %d\nAppuyer sur Espace pour recommencer" % self.game.score)
            self.after_cancel(self.iid_after)

    # Events

    def event_arrow_right(self, event):
        """
        Manages the right arrow keypress event.
        """

        if self.state == states.RUN and \
           self.game.snake.direction != states.WEST:
            self.game.snake.direction = states.EAST

    def event_arrow_left(self, event):
        """
        Manages the left arrow keypress event.
        """

        if self.state == states.RUN and \
           self.game.snake.direction != states.EAST:
            self.game.snake.direction = states.WEST

    def event_arrow_up(self, event):
        """
        Manages the up arrow keypress event.
        """

        if self.state == states.RUN and \
           self.game.snake.direction != states.SOUTH:
            self.game.snake.direction = states.NORTH

    def event_arrow_down(self, event):
        """
        Manages the down arrow keypress event.
        """

        if self.state == states.RUN and \
           self.game.snake.direction != states.NORTH:
            self.game.snake.direction = states.SOUTH

    def event_space(self, event):
        """
        Manages the space keyboard event.
        """

        if self.state == states.PAUSE:
            self.loop()
            self.state = states.RUN
        elif self.state == states.RUN:
            self.after_cancel(self.iid_after)
            self.state = states.PAUSE

        elif self.state == states.END:
            self.init_new_game()


if __name__ == '__main__':
    app = Application()
    app.mainloop()
