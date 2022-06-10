#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import random

from PyQt5.QtCore import QObject, pyqtSignal


class Board(QObject):
    ROWS = 300
    COLS = 300

    on_update_generation = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        # TODO:
        self.matrix: list[list[bool]] = [
            [random.randrange(10) == 0 for _ in range(self.COLS)]
            # TODO:
            # [False for _ in range(self.COLS)]
            for _ in range(self.ROWS)
        ]
        # TODO:
        # x = y = 0
        # self.matrix[x + 0][y + 0] = True
        # self.matrix[x + 0][y + 1] = True
        # self.matrix[x + 1][y + 0] = True
        # # self.matrix[x + 1][y + 1] = True

        self.__generation_number = 0

    @property
    def count_living_cells(self) -> int:
        return sum(sum(row) for row in self.matrix)

    @property
    def generation_number(self) -> int:
        return self.__generation_number

    @generation_number.setter
    def generation_number(self, value: int):
        self.__generation_number = value
        self.on_update_generation.emit(self.generation_number)

    def _check_value(self, row: int, col: int) -> bool:
        if row < 0:
            row = len(self.matrix) - 1

        if row > len(self.matrix) - 1:
            row = 0

        if col < 0:
            col = len(self.matrix[row]) - 1

        if col > len(self.matrix[row]) - 1:
            col = 0

        return self.matrix[row][col]

    def count_neighbors(self, row: int, col: int) -> int:
        return sum((
            self._check_value(row, col - 1),
            self._check_value(row - 1, col - 1),
            self._check_value(row - 1, col),
            self._check_value(row - 1, col + 1),
            self._check_value(row, col + 1),
            self._check_value(row + 1, col + 1),
            self._check_value(row + 1, col),
            self._check_value(row + 1, col - 1),
        ))

    def do_step(self) -> bool:
        self.generation_number += 1

        new_matrix = [
            [False for _ in range(self.COLS)]
            for _ in range(self.ROWS)
        ]

        for i, row in enumerate(self.matrix):
            for j, cell in enumerate(row):
                count = self.count_neighbors(i, j)

                if not cell and count == 3:
                    new_matrix[i][j] = True

                elif cell and count in (2, 3):
                    new_matrix[i][j] = True

        # TODO: Нужно помнить предыдущие состояния или их слепки
        self.matrix = new_matrix

        # TODO: Возвращать False если состояние не поменялось
        return self.count_living_cells > 0
