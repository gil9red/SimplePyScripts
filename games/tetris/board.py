#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QColor

from common import logger
from piece import Piece


class Board(QObject):
    ROWS = 20
    COLS = 10

    on_update_score = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.matrix: list[list[QColor | None]] = [
            [None for _ in range(self.COLS)]
            for _ in range(self.ROWS)
        ]

        self.current_piece: Piece = None
        self.next_piece: Piece = None

        self.__score: int = 0

    @property
    def score(self) -> int:
        return self.__score

    @score.setter
    def score(self, value: int):
        self.__score = value
        self.on_update_score.emit(self.score)

    def add_piece(self, piece: Piece):
        logger.debug("[add_piece]")
        for x, y in piece.get_points():
            self.matrix[y][x] = piece.get_color()

    def _do_make_collapse_of_rows(self):
        to_delete = []
        for row in reversed(self.matrix):
            if all(color for color in row):
                to_delete.append(row)

        for row in to_delete:
            self.matrix.remove(row)
            self.matrix.insert(0, [None for _ in range(self.COLS)])

        # Если были удалены строки
        if to_delete:
            self.score += {1: 100, 2: 300, 3: 700, 4: 1500}[len(to_delete)]

    def _get_random_piece(self) -> Piece:
        return Piece.get_random(
            x=self.COLS // 2,  # По-умолчанию, по центру
            y=0,
            parent=self,
        )

    def do_step(self) -> bool:
        if not self.current_piece:
            if self.next_piece:
                self.current_piece = self.next_piece
            else:
                self.current_piece = self._get_random_piece()

            self.next_piece = self._get_random_piece()

            # Если сразу после создания столкновение
            if self.current_piece.is_collapse():
                return False

            return True

        if not self.current_piece.move_down():
            self.add_piece(self.current_piece)
            self.current_piece = None

            self._do_make_collapse_of_rows()

        return True
