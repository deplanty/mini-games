import tkinter as tk

from src.field import Field
from src import tags


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.state = tags.FIRST_TURN
        self.current_pawn = None

        self.withdraw()
        self.title("Solitaire")
        self.set_menu()
        self.set_ui()
        self.set_events()
        self.resizable(False, False)
        self.init_new_game()
        self.deiconify()

    # UI methods

    def set_ui(self):
        """
        Sets the elements in the UI.
        """

        self.canvas = tk.Canvas(self)
        self.canvas.pack()
        self.field = Field(self.canvas)

    def set_menu(self):
        """
        Sets the menu in the UI.
        """

        menu = tk.Menu(self)
        menu_game = tk.Menu(menu, tearoff=0)
        menu_game.add_command(label="Nouveau", command=self.init_new_game)
        menu.add_cascade(label="Jeu", menu=menu_game)
        self.configure(menu=menu)

    def set_events(self):
        """
        Sets the events in the UI.
        """

        self.canvas.bind("<Button-1>", self.event_left_click)
        self.canvas.bind("<Button-3>", self.event_right_click)

    # Game methods

    def init_new_game(self):
        """
        Initializes a new game/
        """

        self.field.init()
        self.state = tags.FIRST_TURN

    # Events

    def event_left_click(self, event):
        """
        Manages the left click button event.
        """

        # Verify if a box has been clicked
        box = self.field.get(event.x, event.y)
        if not box:
            return

        # First turn : remove a pawn
        if self.state == tags.FIRST_TURN:
            self.field.toggle(box)
            self.field.show_movable_pawns()
            self.state = tags.SELECT_PAWN
        # Select a pawn
        elif self.state == tags.SELECT_PAWN:
            if self.field.box_is(box, tags.PAWN_MOVABLE):
                self.current_pawn = box
                self.field.show_target_box(box)
                self.state = tags.MOVE_PAWN
        # Move the pawn to an empty space
        # and remove the pawn between
        elif self.state == tags.MOVE_PAWN:
            if self.field.box_is(box, tags.EMPTY_TARGET):
                # Move the pawn
                self.field.toggle(box)
                self.field.toggle(self.current_pawn)
                # Remove the middle pawn
                i_box, j_box, _ = self.field.get_info(box)
                i_cur, j_cur, _ = self.field.get_info(self.current_pawn)
                i = (i_box + i_cur) // 2
                j = (j_box + j_cur) // 2
                self.field.toggle(self.field.grid[i][j])
                self.current_pawn = None
                # Show next move
                self.field.show_movable_pawns()
                self.state = tags.SELECT_PAWN
            # Undo pawn selection
            elif box == self.current_pawn:
                self.field.show_movable_pawns()
                self.state = tags.SELECT_PAWN

    def event_right_click(self, event):

        # Verify if a box has been clicked
        box = self.field.get(event.x, event.y)
        if not box:
            return

        self.field.toggle(box)


if __name__ == '__main__':
    app = Application()
    app.mainloop()
