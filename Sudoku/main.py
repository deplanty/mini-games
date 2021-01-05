import tkinter as tk
import tkinter.messagebox
from tkinter import ttk

from src.grid import Grid


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.withdraw()
        self.title("Sudoku")
        self.set_ui()
        # self.set_menu()
        self.set_events()
        self.init_new_game("resources/Facile-1.txt")
        self.resizable(False, False)
        self.deiconify()

    def set_ui(self):
        """
        Sets the elements in the UI.
        """

        self.canvas = tk.Canvas(self)
        self.canvas.pack()

        self.entry = ttk.Entry(self.canvas, justify="center", font=("Calibri", 12))

        self.grid = Grid(self.canvas)

    def set_events(self):
        """
        Sets events in the UI.
        """

        self.canvas.bind("<Button-1>", self.event_click_left)
        self.bind("<Return>", self.event_return)

    # Game methods

    def init_new_game(self, file:str):
        """
        Inits a new game with a grid from a file.
        """

        self.grid.init(file)

    # Events

    def event_click_left(self, event):
        """
        Manages the mouse left button event.
        """

        i, j = self.grid.get_position(event.x, event.y)

        if self.grid[i][j].fixed:
            return

        # Places the entry
        self.entry["text"] = self.grid[i][j]
        self.entry.place(
            x=j * self.grid.box_size + 2,
            y=i * self.grid.box_size + 2,
            width=self.grid.box_size + 1,
            height=self.grid.box_size + 1
        )
        self.entry.focus_set()

    def event_return(self, event):
        """
        Manages the return key event.
        """

        x = self.entry.winfo_x()
        y = self.entry.winfo_y()
        i, j = self.grid.get_position(x, y)
        self.grid.set_value(i, j, self.entry.get())
        self.entry.place_forget()

        win = self.grid.check_grid()
        if win:
            tk.messagebox.showinfo(
                title="Gagné",
                message="Félicitation ! Vous avez réussi !"
            )


if __name__ == '__main__':
    app = Application()
    app.mainloop()
