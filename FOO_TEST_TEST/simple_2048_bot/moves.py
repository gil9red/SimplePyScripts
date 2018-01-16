class Move:
    def __init__(self, dir_y, dir_x, name):
        self.dir = (dir_y, dir_x)
        self.name = name

    def __repr__(self):
        return self.name

    def get_dir(self):
        return self.dir

    def get_move_axis(self):
        return "y" if self.dir[0] else "x"

    def get_static_axis(self):
        return "y" if self.get_move_axis() == "x" else "x"

UP = Move(-1, 0, "UP")
DOWN = Move(1, 0, "DOWN")
RIGHT = Move(0, 1, "RIGHT")
LEFT = Move(0, -1, "LEFT")

ALL_MOVES = (UP, DOWN, RIGHT, LEFT)
