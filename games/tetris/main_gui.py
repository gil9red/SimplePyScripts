#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import functools
import sys
import traceback

from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt5.QtGui import QPainter, QPaintEvent, QKeyEvent, QColor
from PyQt5.QtCore import Qt, QTimer, QSize

from core.board import Board
from core.common import logger
from core.piece import Piece


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    logger.error(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


def painter_context(func):
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        painter: QPainter | None = None
        for arg in args + tuple(kwargs.values()):
            if isinstance(arg, QPainter):
                painter = arg
                break

        if painter:
            painter.save()
        try:
            return func(*args, **kwargs)
        finally:
            if painter:
                painter.restore()

    return decorated


class MainWindow(QWidget):
    CELL_SIZE: int = 20
    INDENT: int = 10

    SPEED_MS: int = 400

    TITLE: str = "Tetris"

    def __init__(self):
        super().__init__()

        self.board = Board()
        self.board.on_update_score.connect(self._update_states)

        self.current_piece: Piece | None = None
        self.next_piece: Piece | None = None

        self.timer = QTimer()
        self.timer.timeout.connect(self._on_tick)
        self.timer.setInterval(self.SPEED_MS)
        self.timer.start()

        self._update_states()

    def sizeHint(self) -> QSize:
        columns = len(self.board.matrix[0])
        width = self.CELL_SIZE * columns
        width += self.INDENT * 2

        added_panel_cells: int = 6
        width += self.CELL_SIZE * added_panel_cells

        rows = len(self.board.matrix)
        height = self.CELL_SIZE * rows + self.INDENT * 2
        return QSize(width, height)

    def _update_states(self):
        self.setWindowTitle(
            f"{self.TITLE}. Score: {self.board.score}{'' if self.timer.isActive() else '. Paused'}"
        )

    def abort_game(self):
        self.timer.stop()
        QMessageBox.information(self, "Информация", "Проигрыш!")

    def _on_logic(self):
        if not self.board.do_step():
            self.abort_game()
            return

        self.current_piece = self.board.current_piece
        self.next_piece = self.board.next_piece

    def _on_tick(self):
        self._on_logic()
        self._update_states()
        self.update()

    def _draw_cell_board(self, painter: QPainter, x: int, y: int, color: QColor):
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        painter.drawRect(
            x * self.CELL_SIZE + self.INDENT,
            y * self.CELL_SIZE + self.INDENT,
            self.CELL_SIZE,
            self.CELL_SIZE,
        )

    @painter_context
    def _draw_board(self, painter: QPainter):
        # Рисование заполненных ячеек
        for y, row in enumerate(self.board.matrix):
            for x, cell_color in enumerate(row):
                if not cell_color:
                    continue

                self._draw_cell_board(painter, x, y, cell_color)

        painter.setPen(Qt.black)

        # Горизонтальные линии
        y1 = y2 = self.INDENT
        x1 = self.INDENT
        x2 = self.CELL_SIZE * self.board.COLS + self.INDENT
        for i in range(self.board.ROWS + 1):
            painter.drawLine(x1, y1, x2, y2)
            y1 += self.CELL_SIZE
            y2 += self.CELL_SIZE

        # Вертикальные линии
        x1 = x2 = self.INDENT
        y1 = self.INDENT
        y2 = self.CELL_SIZE * self.board.ROWS + self.INDENT
        for i in range(self.board.COLS + 1):
            painter.drawLine(x1, y1, x2, y2)
            x1 += self.CELL_SIZE
            x2 += self.CELL_SIZE

    @painter_context
    def _draw_current_piece(self, painter: QPainter):
        if not self.current_piece:
            return

        for x, y in self.current_piece.get_points():
            self._draw_cell_board(painter, x, y, self.current_piece.get_color())

    @painter_context
    def _draw_shadow_of_current_piece(self, painter: QPainter):
        if not self.current_piece:
            return

        points: list[tuple[int, int]] = self.current_piece.get_points()

        color: QColor = self.current_piece.get_color()
        color.setAlphaF(0.2)

        # Рисование тени
        for y, row in enumerate(self.board.matrix):
            for x, _ in enumerate(row):
                max_piece_y = max((py for px, py in points if px == x), default=-1)

                min_field_y = -1
                for y_, row_ in enumerate(self.board.matrix):
                    cell_color: QColor | None = row_[x]
                    if not cell_color:
                        continue

                    min_field_y = y_
                    break

                if y <= max_piece_y or (min_field_y != -1 and y >= min_field_y):
                    continue

                if (
                    x < self.current_piece.get_min_x()
                    or x > self.current_piece.get_max_x()
                ):
                    continue

                self._draw_cell_board(painter, x, y, color)

    @painter_context
    def _draw_next_piece(self, painter: QPainter):
        if not self.next_piece:
            return

        x_next = self.board.COLS + 3
        y_next = 1
        for x, y in self.next_piece.get_points_for_state(x=x_next, y=y_next):
            self._draw_cell_board(painter, x, y, self.next_piece.get_color())

    @painter_context
    def _draw_score(self, painter: QPainter):
        painter.setPen(Qt.black)

        x = self.CELL_SIZE * (self.board.COLS + 1) + self.INDENT
        y = self.CELL_SIZE * 5 + self.INDENT
        painter.drawText(x, y, f"Score: {self.board.score}")

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self._draw_current_piece(painter)
        self._draw_shadow_of_current_piece(painter)
        self._draw_board(painter)
        self._draw_next_piece(painter)
        self._draw_score(painter)

    def keyReleaseEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Space:
            if self.timer.isActive():
                self.timer.stop()
            else:
                self.timer.start()

            self._update_states()
            return

        if self.current_piece and self.timer.isActive():
            match event.key():
                case Qt.Key_Left:
                    self.current_piece.move_left()

                case Qt.Key_Right:
                    self.current_piece.move_right()

                case Qt.Key_Up:
                    self.current_piece.turn()

                case Qt.Key_Down:
                    while self.current_piece.move_down():
                        pass

            self.update()
            return


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
