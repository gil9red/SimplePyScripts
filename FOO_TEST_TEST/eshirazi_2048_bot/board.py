import itertools
import random


from eshirazi_2048_bot.config import BOARD_SIZE
from eshirazi_2048_bot.helpers import irange
from eshirazi_2048_bot.moves import ALL_MOVES

ALL_TILES = list(itertools.product(irange(BOARD_SIZE), irange(BOARD_SIZE)))
POSSIBLE_NEW_TILES = [4] + ([2] * 9)


class IllegalMoveException(Exception):
    pass


class Board:
    b = None

    def clear(self):
        self.b = [
            [0 for _ in irange(BOARD_SIZE)]
            for _ in irange(BOARD_SIZE)
        ]

    def __init__(self, init_board=None, ):
        if init_board is None:
            # Create a new empty board
            self.clear()

            # Initialize it with 2, 2 or 2, 4
            initializers = list(random.choice([
                (2, 4),
                (2, 2)
            ]))

            for y, x in random.sample(ALL_TILES, len(initializers)):
                self[y, x] = initializers.pop()

        elif isinstance(init_board, Board):
            # Copy constructor
            self.b = [
                [
                    init_board[y, x]
                    for x in irange(BOARD_SIZE)
                ]
                for y in irange(BOARD_SIZE)
            ]

        else:
            # Copy from lists
            self.b = [
                [
                    init_board[y][x]
                    for x in irange(BOARD_SIZE)
                ]
                for y in irange(BOARD_SIZE)
            ]

    def __getitem__(self, indices):
        return self.b[indices[0]][indices[1]]

    def __setitem__(self, indices, value):
        self.b[indices[0]][indices[1]] = value

    def __repr__(self):
        cell_size = max(len(str(self[y, x])) for y, x in ALL_TILES)
        line_size = (cell_size + 1) * BOARD_SIZE
        sap_line = "+".join("-" * (cell_size + 2) for i in irange(BOARD_SIZE))

        ret = ""
        for y in irange(BOARD_SIZE):
            for x in irange(BOARD_SIZE):
                if self[y, x] != 0:
                    ret += " " + (" " * cell_size + str(self[y, x]))[-cell_size:] + " "
                else:
                    ret += " " * (cell_size + 2)

                if x != BOARD_SIZE - 1:
                    ret += "|"

            if y != BOARD_SIZE - 1:

                ret += "\n" + sap_line + "\n"
        return ret + "\n"

    def move_only_swipe(self, move):
        move_axis = move.get_move_axis()
        static_axis = move.get_static_axis()
        direction = sum(move.get_dir())

        done_something = False

        adapt = \
            lambda i: \
            i if direction != 1 else (BOARD_SIZE - i - 1)

        conv_i_j = \
            lambda i, j: \
            (
                i if static_axis == "y" else adapt(j),
                adapt(j) if move_axis == "x" else i
            )

        def get(i, j):
            return self[conv_i_j(i, j)]

        def put(i, j, value):
            self[conv_i_j(i, j)] = value

        for i in irange(BOARD_SIZE):
            last_stumbled = None
            last_stumbled_idx = None
            first_free_idx = None

            for j in irange(BOARD_SIZE):
                cur = get(i, j)

                if cur != 0:
                    if last_stumbled == cur:
                        put(i, j, 0)
                        put(i, last_stumbled_idx, cur * 2)
                        first_free_idx = last_stumbled_idx + 1
                        last_stumbled = None
                        last_stumbled_idx = None
                        done_something = True
                    elif first_free_idx is not None:
                        put(i, j, 0)
                        put(i, first_free_idx, cur)
                        last_stumbled = cur
                        last_stumbled_idx = first_free_idx
                        first_free_idx += 1
                        done_something = True
                    else:
                        last_stumbled_idx = j
                        last_stumbled = cur
                elif first_free_idx is None:
                    first_free_idx = j

        if not done_something:
            raise IllegalMoveException

    def get_legal_moves(self):
        ret = []
        for move in ALL_MOVES:
            try:
                Board(self).move_only_swipe(move)
                ret.append(move)
            except IllegalMoveException:
                continue

        return ret

    def has_legal_moves(self):
        return bool(self.get_legal_moves())

    def add_random_tile(self):
        try:
            self[random.choice(tuple(self.get_free_tiles()))] = random.choice(POSSIBLE_NEW_TILES)
        except IndexError:
            raise IllegalMoveException()

    def move(self, move):
        self.move_only_swipe(move)
        self.add_random_tile()

    def has_tile(self, value):
        for y, x in ALL_TILES:
            if self[y, x] == value:
                return True

        return False

    def get_max_tile(self):
        return max(self[y, x] for y, x in ALL_TILES)

    def get_free_tiles(self):
        return ((y, x) for y, x in ALL_TILES if self[y, x] == 0)

    def get_num_free_tiles(self):
        return sum(1 for _ in self.get_free_tiles())
