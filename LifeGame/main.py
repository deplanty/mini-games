import tkinter as tk
from tkinter import ttk

from src.grid import Grid


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # Field size
        self.grid_size = (16, 16)

        self.state = "pause"
        self.state_id = None

        self.var_ms = tk.IntVar(self, 300)

        self.withdraw()
        self.title("Life Game")
        # self.set_menu()
        self.set_ui()
        self.set_events()
        self.resizable(False, False)
        self.init_new_game()
        self.deiconify()

    def set_ui(self):
        """
        Sets the elements in the UI.
        """

        f = tk.Frame(self)
        f.pack(fill="both", expand=True)

        self.b_start = ttk.Button(f, text="Démarrer", command=self.btn_run_pause)
        self.b_start.pack(side="left", padx=5, pady=5)
        self.b_reset = ttk.Button(f, text="Recommencer", command=self.btn_reset)
        self.b_reset.pack(side="left", padx=5, pady=5)
        self.s_ms = tk.Scale(f, from_=10, to=1000, resolution=10, variable=self.var_ms, orient="horizontal")
        self.s_ms.pack(side="left", padx=5, pady=5)
        # self.l_ms = ttk.Label()

        self.canvas = tk.Canvas()
        self.canvas.pack()
        self.field = Grid(self.canvas)

    def set_events(self):
        """
        Sets the events in the UI.
        """

        self.bind("<space>", self.event_space)
        self.canvas.bind("<Button-1>", self.event_left_click)

    def init_new_game(self):
        """
        Initializes a new field
        """

        # Clear previous game
        self.field.init(self.grid_size)
        self.focus_set()

    def loop(self):
        """
        Loops
        """

        for box in self.field.gen_boxes():
            self.field.process_box(box)

        self.field.apply()

        self.state_id = self.after(self.var_ms.get(), self.loop)

    # Boutons

    def btn_run_pause(self):
        """
        Runs or pauses the loop.
        """

        self.event_space()

    def btn_reset(self):
        """
        Resets all boxes.
        """

        if self.state == "pause":
            self.init_new_game()

    # Events

    def event_space(self, event=None):
        """
        Manages the event when pressing space bar
        """

        if self.state == "pause":
            self.state = "run"
            self.b_start.configure(text="Pause")
            self.focus_set()
            self.loop()
        elif self.state == "run":
            self.state = "pause"
            self.b_start.configure(text="Démarrer")
            self.focus_set()
            self.after_cancel(self.state_id)

    def event_left_click(self, event=None):
        """
        Manages tje event when pressing left click
        """

        # Can modify field only when paused
        if self.state == "pause":
            i = event.y // self.field.box_size
            j = event.x // self.field.box_size
            self.field.toggle(i, j)



if __name__ == '__main__':
    app = Application()
    app.mainloop()
