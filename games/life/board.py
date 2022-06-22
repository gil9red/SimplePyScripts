#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import enum
from itertools import cycle
from typing import Iterator

from PyQt5.QtCore import QObject, pyqtSignal

from world_seed_in_binary_2D import get_bits_seed, get_random_seed


class StepResultEnum(enum.Enum):
    OK = enum.auto()
    NO_CELLS = enum.auto()
    NO_CHANGE = enum.auto()
    REPEATS = enum.auto()


class Board(QObject):
    ROWS = 100
    COLS = 100

    on_update_generation = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.seed = ''
        self.matrix: list[list[bool]] = []
        self.matrix_digest_list: list[int] = []
        self.__generation_number = 0

    def generate(self, seed: str = ''):
        self.seed = seed
        if not self.seed:
            self.seed = get_random_seed()

        bits: str = get_bits_seed(self.seed)
        seqs: Iterator[str] = cycle(bits + bits[::-1])

        self.matrix = [
            [next(seqs) == '1' for _ in range(self.COLS)]
            for _ in range(self.ROWS)
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
                    items.append(f'{i}x{j}')

        return hash(','.join(items))

    def do_step(self) -> StepResultEnum:
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

        self.matrix = new_matrix

        if self.count_living_cells <= 0:
            return StepResultEnum.NO_CELLS

        digest = self.get_matrix_digest(self.matrix)

        if self.matrix_digest_list:
            if self.matrix_digest_list[-1] == digest:
                return StepResultEnum.NO_CHANGE

            if digest in self.matrix_digest_list:
                return StepResultEnum.REPEATS

        self.matrix_digest_list.append(digest)

        return StepResultEnum.OK
