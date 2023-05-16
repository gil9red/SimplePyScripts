#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import enum
import random
import string

from PyQt5.QtCore import QObject, pyqtSignal


def get_random_seed(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


class StepResultEnum(enum.Enum):
    OK = enum.auto()
    NO_CELLS = enum.auto()
    NO_CHANGE = enum.auto()
    REPEATS = enum.auto()


class Board(QObject):
    on_update_generation = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.rows = 100
        self.cols = 100

        self.seed = ""
        self.matrix: list[list[bool]] = []
        self.matrix_digest_list: list[int] = []
        self.__generation_number = 0

        self.last_step_result: StepResultEnum = None

    def generate(self, seed: str = ""):
        self.seed = seed
        if not self.seed:
            self.seed = get_random_seed()

        random.seed(self.seed)

        self.matrix = [
            [random.randrange(5) == 0 for _ in range(self.cols)]
            for _ in range(self.rows)
        ]

        self.matrix_digest_list.clear()
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

    @classmethod
    def get_matrix_digest(cls, matrix: list[list[bool]]) -> int:
        items = []
        for i, row in enumerate(matrix):
            for j, cell in enumerate(row):
                if cell:
                    items.append(f"{i}x{j}")

        return hash(",".join(items))

    def do_step(self) -> StepResultEnum:
        self.generation_number += 1

        new_matrix = [
            [False for _ in range(self.cols)]
            for _ in range(self.rows)
        ]

        for i, row in enumerate(self.matrix):
            for j, cell in enumerate(row):
                count = self.count_neighbors(i, j)

                if not cell and count == 3:
                    new_matrix[i][j] = True

                elif cell and count in (2, 3):
                    new_matrix[i][j] = True

        self.matrix = new_matrix

        if self.count_living_cells <= 0:
            self.last_step_result = StepResultEnum.NO_CELLS
            return self.last_step_result

        digest = self.get_matrix_digest(self.matrix)

        if self.matrix_digest_list:
            if self.matrix_digest_list[-1] == digest:
                self.last_step_result = StepResultEnum.NO_CHANGE
                return self.last_step_result

            if digest in self.matrix_digest_list:
                self.last_step_result = StepResultEnum.REPEATS
                return self.last_step_result

        self.matrix_digest_list.append(digest)

        self.last_step_result = StepResultEnum.OK
        return self.last_step_result
