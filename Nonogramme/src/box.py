from src import states


class Box:
    def __init__(self, value:str):
        self.s = value
        self.iid = None
        self.state = states.HIDDEN

