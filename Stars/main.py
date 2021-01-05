import json
import tkinter as tk
from tkinter import ttk

from src.frames.ui_main import UI_Main
from src.objects import Asteroid, Star


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.fps = 60  # Frame / s
        self.mspf = 1000 / self. fps  # ms / frame

        self.asteroid = None
        self.stars = list()

        self.iid_after = None

        self.withdraw()
        self.title("Stars")
        self.set_style()
        self.set_ui()
        self.resizable(False, False)
        self.init_new_game()
        self.deiconify()

    # UI

    def set_style(self):
        """
        Sets the styles of the elements in the UI.
        """

        with open("resources/styles_ttk.json") as fid:
            styles = json.load(fid)

        self.style = ttk.Style(self)
        for style, params in styles.items():
            self.style.configure(style, **params)

    def set_ui(self):
        """
        Sets UI in the window.
        """

        self.ui = UI_Main(self)
        self.ui.pack()
        self.ui.canvas.configure(width=840, height=680)

        self.ui.button.configure(command=self.ask_asteroid)

    # Game

    def init_new_game(self):
        """
        Initializes a new game
        """

        # Reset all
        if self.iid_after:
            self.after_cancel(self.iid_after)
            self.iid_after = None

        for star in self.stars:
            self.ui.canvas.delete(star.iid)
        self.stars.clear()

        if self.asteroid:
            self.ui.canvas.delete(self.asteroid.iid, self.asteroid.iid_arrow)
            self.asteroid = None

        # Ask user to place items on screen
        self.ask_stars()

    def ask_stars(self):
        """
        Asks the player to place stars on screen.
        """

        self.ui.button.configure(text="Continuer", command=self.ask_asteroid)
        self.ui.label.configure(text="Placez les étoiles")
        self.ui.canvas.bind("<Button-1>", self.event_ask_stars)

    def ask_asteroid(self):
        """
        Asks the player to place an asteroid on screen.
        """

        self.ui.label.configure(text="Placez votre astéroïde")
        self.ui.canvas.bind("<Button-1>", self.event_ask_asteroid)

    def ask_speed(self):
        """
        Asks the player the speed of the asteroid.
        """

        self.ui.label.configure(text="Choisissez votre vitesse de départ")
        self.ui.canvas.bind("<Motion>", self.event_ask_speed)
        self.ui.canvas.bind("<Button-1>", self.event_select_speed)

    def loop(self):
        """
        Processes the game loop.
        """

        dt = self.mspf / 1000
        self.asteroid.move(dt, self.stars)

        self.iid_after = self.after(int(self.mspf), self.loop)

    # Events

    def event_ask_stars(self, event):
        """
        Adds stars on the canvas.
        """

        star = Star(self.ui.canvas, event.x, event.y, 10, 2e15)
        star.init()
        self.stars.append(star)

    def event_ask_asteroid(self, event):
        """
        Adds an asteroid on the canvas.
        """

        self.asteroid = Asteroid(self.ui.canvas, event.x, event.y, 7)
        self.asteroid.init()

        self.ask_speed()

    def event_ask_speed(self, event):
        """
        Shows the speed on screen.
        """

        self.asteroid.v_x = (event.x - self.asteroid.x) / 10
        self.asteroid.v_y = (event.y - self.asteroid.y) / 10
        self.asteroid.update_draw()

    def event_select_speed(self, event):
        """
        Selects the speed for the asteroid.
        """

        self.ui.canvas.unbind("<Motion>")
        self.ui.canvas.unbind("<Button-1>")
        self.loop()

        self.ui.label.configure(text="")
        self.ui.button.configure(text="Recommencer", command=self.init_new_game)



if __name__ == '__main__':
    app = Application()
    app.mainloop()
