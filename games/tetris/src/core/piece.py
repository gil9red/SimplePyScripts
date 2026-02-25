#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import abc
from random import choice, randrange

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from .common import logger


class Piece(abc.ABC):
    STATES: dict[int, int] = {
        1: 2,
        2: 3,
        3: 4,
        4: 1,
    }

    def __init__(self, x: int, y: int, parent: "Board" = None) -> None:
        self.x = x
        self.y = y
        self.parent = parent

        self.current_state: int = 1
        self.points: list[tuple[int, int]] = self.get_points_for_state()

    @classmethod
    def get_random(
        cls,
        x: int,
        y: int,
        parent: "Board",
        rand_x: bool = False,
    ) -> "Piece":
        clazz = choice(cls.__subclasses__())
        obj = clazz(x=x, y=y, parent=parent)

        # Переместим фигуру рандомно влево или вправо
        if rand_x:
            move_func = choice([obj.move_left, obj.move_right])
            for _ in range(randrange(0, parent.COLS // 2)):
                if not move_func():
                    break

        return obj

    @abc.abstractmethod
    def get_color(self) -> QColor:
        pass

    @abc.abstractmethod
    def _get_all_states(self) -> list[list[str]]:
        pass

    def get_points_for_state(
        self,
        state: int = None,
        x: int = None,
        y: int = None,
    ) -> list[tuple[int, int]]:
        if state is None:
            state = self.current_state

        if x is None:
            x = self.x

        if y is None:
            y = self.y

        if state not in (1, 2, 3, 4):
            raise Exception(f"Unknown state {state}!")

        # Учитываем количество состояний в points_board - нужно менять значение state:
        #   * Для одного - всегда первый
        #   * Для двух - нечетный/четный
        #   * Для четырех - не нужно ничего делать
        all_states = self._get_all_states()
        number_of_states = len(all_states)
        if number_of_states == 1:  # Например, для квадрата
            state = 0
        elif number_of_states == 2:
            state = state % 2 == 0
        else:
            state = state - 1

        points_board = all_states[state]

        idx_x = idx_y = -1
        for i, row in enumerate(points_board):
            for j, value in enumerate(row):
                if value == "X":
                    idx_x = j
                    idx_y = i
                    break

        points = []
        for i, row in enumerate(points_board):
            for j, value in enumerate(row):
                if value != ".":
                    points.append(
                        (
                            # Рассчитываем разницу между X и остальными значениями
                            # и прибавляем текущие координаты центра фигуры
                            (j - idx_x) + x,
                            (i - idx_y) + y,
                        )
                    )
        return points

    def get_min_x(self) -> int:
        return min(x for x, _ in self.get_points())

    def get_max_x(self) -> int:
        return max(x for x, _ in self.get_points())

    def get_min_y(self) -> int:
        return min(y for _, y in self.get_points())

    def get_max_y(self) -> int:
        return max(y for _, y in self.get_points())

    def go_to_next_state(self) -> None:
        self.current_state = self.STATES[self.current_state]

    def set_points(self, points: list[tuple[int, int]]) -> None:
        self.points = points

    def get_points(self) -> list[tuple[int, int]]:
        return self.points

    def move_left(self) -> bool:
        x = self.x - 1
        points = self.get_points_for_state(x=x)
        if self.is_collapse(points):
            return False

        self.x = x
        self.set_points(points)
        return True

    def move_right(self) -> bool:
        x = self.x + 1
        points = self.get_points_for_state(x=x)
        if self.is_collapse(points):
            return False

        self.x = x
        self.set_points(points)
        return True

    def move_down(self) -> bool:
        y = self.y + 1
        points = self.get_points_for_state(y=y)
        if self.is_collapse(points):
            return False

        self.y = y
        self.set_points(points)
        return True

    def _on_turn_right(self, for_state: int = None) -> list[tuple[int, int]]:
        return self.get_points_for_state(for_state)

    def turn(self) -> bool:
        state = self.STATES[self.current_state]
        points = self._on_turn_right(for_state=state)
        if self.is_collapse(points):
            return False

        self.go_to_next_state()
        self.set_points(points)
        return True

    def is_collapse(self, points: list[tuple[int, int]] = None) -> bool:
        if not points:
            points = self.get_points()

        for x, y in points:
            try:
                if x < 0 or y < 0:
                    logger.debug(f"[is_collapse] y < 0 or x < 0. x={x}, y={y}")
                    return True

                # Если ячейка занята или выход за пределы
                if self.parent.matrix[y][x]:
                    logger.debug(
                        f"[is_collapse] self.parent.board_matrix[y][x]. x={x}, y={y}, "
                        f"value={self.parent.matrix[y][x]}"
                    )
                    return True

            except IndexError:
                logger.debug(f"[is_collapse] IndexError. x={x}, y={y}")
                return True

        return False


class PieceO(Piece):
    _ = [
        [
            "....",
            ".1X.",
            ".11.",
            "....",
        ],
    ]

    def _get_all_states(self) -> list[list[str]]:
        return self._

    def get_color(self) -> QColor:
        return QColor(Qt.yellow)


class PieceI(Piece):
    _ = [
        [
            "....",
            "11X1",
            "....",
            "....",
        ],
        [
            "..1.",
            "..X.",
            "..1.",
            "..1.",
        ],
    ]

    def _get_all_states(self) -> list[list[str]]:
        return self._

    def get_color(self) -> QColor:
        return QColor("#7F00FF")  # Violet


class PieceS(Piece):
    _ = [
        [
            "....",
            "..X1",
            ".11.",
            "....",
        ],
        [
            "..1.",
            "..X1",
            "...1",
            "....",
        ],
    ]

    def _get_all_states(self) -> list[list[str]]:
        return self._

    def get_color(self) -> QColor:
        return QColor(Qt.green)


class PieceZ(Piece):
    _ = [
        [
            "....",
            ".1X.",
            "..11",
            "....",
        ],
        [
            "...1",
            "..X1",
            "..1.",
            "....",
        ],
    ]

    def _get_all_states(self) -> list[list[str]]:
        return self._

    def get_color(self) -> QColor:
        return QColor(Qt.red)


class PieceL(Piece):
    _ = [
        [
            "....",
            ".1X1",
            ".1..",
            "....",
        ],
        [
            "..1.",
            "..X.",
            "..11",
            "....",
        ],
        [
            "...1",
            ".1X1",
            "....",
            "....",
        ],
        [
            ".11.",
            "..X.",
            "..1.",
            "....",
        ],
    ]

    def _get_all_states(self) -> list[list[str]]:
        return self._

    def get_color(self) -> QColor:
        return QColor(Qt.blue)


class PieceJ(Piece):
    _ = [
        [
            "....",
            ".1X1",
            "...1",
            "....",
        ],
        [
            "..11",
            "..X.",
            "..1.",
            "....",
        ],
        [
            ".1..",
            ".1X1",
            "....",
            "....",
        ],
        [
            "..1.",
            "..X.",
            ".11.",
            "....",
        ],
    ]

    def _get_all_states(self) -> list[list[str]]:
        return self._

    def get_color(self) -> QColor:
        return QColor(Qt.darkGreen)


class PieceT(Piece):
    _ = [
        [
            "....",
            ".1X1",
            "..1.",
            "....",
        ],
        [
            "..1.",
            "..X1",
            "..1.",
            "....",
        ],
        [
            "..1.",
            ".1X1",
            "....",
            "....",
        ],
        [
            "..1.",
            ".1X.",
            "..1.",
            "....",
        ],
    ]

    def _get_all_states(self) -> list[list[str]]:
        return self._

    def get_color(self) -> QColor:
        return QColor(Qt.darkCyan)
