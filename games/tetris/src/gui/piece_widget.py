#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPaintEvent, QPainter
from PyQt5.QtWidgets import QWidget

from ..core.piece import Piece
from .common import CELL_SIZE, draw_cell_board


class PieceWidget(QWidget):
    INDENT: int = 1

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.piece: Piece | None = None

    def set_piece(self, piece: Piece) -> None:
        self.piece = piece
        self.update()

    def minimumSizeHint(self) -> QSize:
        size = (CELL_SIZE * 4) + (self.INDENT * 2)
        return QSize(size, size)

    def paintEvent(self, event: QPaintEvent) -> None:
        if not self.piece:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for x, y in self.piece.get_points_for_state(x=2, y=1):
            draw_cell_board(painter, x, y, self.piece.get_color(), pen=Qt.black)
