import itertools
import random
import tkinter as tk
import tkinter.messagebox

from src.grid import Grid


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.bomb_percent = 0.15

        self.withdraw()
        self.title("Sweeper")
        self.set_menu()
        self.set_ui()
        self.init_new_game()
        self.set_events()
        self.resizable(False, False)
        self.deiconify()

    def set_menu(self):
        """
        Sets the menu in the UI
        """

        self.var_menu_size = tk.IntVar(self, 0)

        menu = tk.Menu(self)
        menu_game = tk.Menu(menu, tearoff=0)
        menu_game.add_command(label="Nouveau", command=self.init_new_game)
        menu_game.add_separator()
        menu_game.add_radiobutton(label="8x8", value=0, variable=self.var_menu_size, command=self.init_new_game)
        menu_game.add_radiobutton(label="16x16", value=1, variable=self.var_menu_size, command=self.init_new_game)
        menu_game.add_radiobutton(label="32x32", value=2, variable=self.var_menu_size, command=self.init_new_game)
        menu.add_cascade(label="Jeu", menu=menu_game)
        self.configure(menu=menu)

    def set_ui(self):
        """
        Sets the structure of the ui
        """

        self.canvas = tk.Canvas(self)
        self.canvas.pack()
        self.field = Grid(self.canvas)

    def set_events(self):
        """
        Sets events in the ui
        """

        self.bind("<KeyPress-a>", self.cheat_show_all)
        self.bind("<KeyPress-b>", self.cheat_show_bombs)
        self.bind("<KeyRelease-b>", self.cheat_hide_bombs)
        self.canvas.bind("<Button-1>", self.event_click_left)
        self.canvas.bind("<Button-3>", self.event_click_right)

    def init_new_game(self):
        """
        Initializes a new game

        - clear previous game
        - create grid
        - add bombs
        """

        # Create new game grid
        grid_size = {
            0: (8, 8),
            1: (16, 16),
            2: (32, 32)
        }.get(self.var_menu_size.get())

        # Clear previous game
        self.field.init(grid_size)

        # Add bombs
        bombs = itertools.product(range(grid_size[0]), range(grid_size[1]))
        n = grid_size[0] * grid_size[1]
        bombs = random.choices(list(bombs), k=int(n*self.bomb_percent))

        for i, j in bombs:
            self.field.set_bomb(i, j)
        self.field.process_values()

    # Events

    def event_click_left(self, event, *args):
        """
        Manage the left-click event
        """

        result = self.field.clicked(event.x, event.y)

        # Lost
        if result == -1:
            self.cheat_show_bombs()
            tk.messagebox.showerror(
                title="Perdu",
                message="Vous avez perdu !"
            )
            self.init_new_game()
            return

        if self.field.has_win():
            self.cheat_show_bombs()
            tk.messagebox.showinfo(
                title="Gagné",
                message="Vous avez gagné !"
            )
            self.init_new_game()
            return

    def event_click_right(self, event, *args):
        """
        Manage the right-click event
        """

        self.field.flag(event.x, event.y)

    # Cheat codes

    def cheat_show_bombs(self, *args):
        """
        Shows bombs
        """

        for box in self.field.list_boxes():
            if box.is_bomb():
                self.canvas.itemconfigure(box.iid, outline="red")

    def cheat_hide_bombs(self, *args):
        """
        Shows bombs
        """

        for box in self.field.list_boxes():
            if box.is_bomb():
                self.canvas.itemconfigure(box.iid, outline="#A0B0A0")

    def cheat_show_all(self, *args):
        """
        Shows all
        """

        for box in self.field.list_boxes():
            if box.is_bomb():
                self.canvas.itemconfigure(box.iid, outline="red")
            else:
                self.field.show_box(box)


if __name__ == '__main__':
    app = Application()
    app.mainloop()
