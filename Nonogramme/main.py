import json
import tkinter as tk
import tkinter.messagebox

from src.view import View
from create import CreateNono


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.withdraw()
        self.title("Nonogramme")
        self.set_ui()
        self.set_menu()
        self.set_events()
        self.init_new_game("resources/A.txt")
        self.resizable(False, False)
        self.deiconify()

        app = CreateNono()
        app.mainloop()

    # UI

    def set_ui(self):
        """
        Sets the elements in the UI.
        """

        self.canvas = tk.Canvas(self)
        self.canvas.pack()

        self.view = View(self.canvas)

    def set_menu(self):
        """
        Sets the menu in the UI.
        """

        # Load the menu organisation
        with open("resources/menu.json") as fid:
            menu_org = json.load(fid)

        self.var_menu_size = tk.IntVar(self, 0)

        menu = tk.Menu(self)
        for menu_label in menu_org:
            menu_tmp = tk.Menu(menu, tearoff=False)
            for label, file in menu_org[menu_label].items():
                menu_tmp.add_command(label=label, command=lambda x=file: self.init_new_game(x))
            menu.add_cascade(label=menu_label, menu=menu_tmp)

        # menu_game = tk.Menu(menu, tearoff=0)
        # menu_game.add_command(label="Nouveau", command=self.init_new_game)
        # menu.add_cascade(label="Jeu", menu=menu_game)
        self.configure(menu=menu)

    def set_events(self):
        """
        Sets the events in the UI.
        """

        self.canvas.bind("<Button-1>", self.event_click_left)

    # Game methods

    def init_new_game(self, file:str):
        """
        Initializes a new game from a file.
        """

        self.view.init(file)

    # Events

    def event_click_left(self, event):
        """
        Manages the mouse left click event.
        """

        self.view.toggle(event.x, event.y)
        win = self.view.check_win()
        if win:
            tk.messagebox.showinfo(
                title="Gagné",
                message="Félicitation ! Vous avez réussi !"
            )


if __name__ == '__main__':
    app = Application()
    app.mainloop()
