#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import functools
import sys
import traceback
from typing import Callable

from PyQt5.QtCore import Qt, QTimer, QSize, pyqtSignal
from PyQt5.QtGui import QPainter, QPaintEvent, QKeyEvent, QColor
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGridLayout,
    QToolButton,
)

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


def painter_context(func: Callable):
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


CELL_SIZE: int = 20


def draw_cell_board(
    painter: QPainter,
    x: int,
    y: int,
    color: QColor,
    pen: Qt.GlobalColor = Qt.NoPen,
    cell_size: int = CELL_SIZE,
    indent: int = 0,
):
    painter.setPen(pen)
    painter.setBrush(color)
    painter.drawRect(
        (x * cell_size) + indent,
        (y * cell_size) + indent,
        cell_size,
        cell_size,
    )


class PieceWidget(QWidget):
    INDENT: int = 1

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.piece: Piece | None = None

    def set_piece(self, piece: Piece):
        self.piece = piece
        self.update()

    def minimumSizeHint(self) -> QSize:
        size = (CELL_SIZE * 4) + (self.INDENT * 2)
        return QSize(size, size)

    def paintEvent(self, event: QPaintEvent):
        if not self.piece:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for x, y in self.piece.get_points_for_state(x=2, y=1):
            draw_cell_board(painter, x, y, self.piece.get_color(), pen=Qt.black)


class BoardWidget(QWidget):
    INDENT: int = 1
    SPEED_MS: int = 400

    on_finish = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.board = Board()

        self.current_piece: Piece | None = None
        self.next_piece: Piece | None = None

        self.timer = QTimer()
        self.timer.timeout.connect(self._on_tick)
        self.timer.setInterval(self.SPEED_MS)
        self.timer.start()

    def minimumSizeHint(self) -> QSize:
        columns = len(self.board.matrix[0])
        width = CELL_SIZE * columns
        width += self.INDENT * 2

        rows = len(self.board.matrix)
        height = (CELL_SIZE * rows) + (self.INDENT * 2)
        return QSize(width, height)

    def abort_game(self):
        self.timer.stop()
        self.on_finish.emit()

    def _on_logic(self):
        if not self.board.do_step():
            self.abort_game()
            return

        self.current_piece = self.board.current_piece
        self.next_piece = self.board.next_piece

    def _on_tick(self):
        self._on_logic()
        self.update()

    @painter_context
    def _draw_board(self, painter: QPainter):
        # Рисование заполненных ячеек
        for y, row in enumerate(self.board.matrix):
            for x, cell_color in enumerate(row):
                if not cell_color:
                    continue

                draw_cell_board(painter, x, y, cell_color, indent=self.INDENT)

        painter.setPen(Qt.black)

        # Горизонтальные линии
        y1 = y2 = self.INDENT
        x1 = self.INDENT
        x2 = CELL_SIZE * self.board.COLS + self.INDENT
        for i in range(self.board.ROWS + 1):
            painter.drawLine(x1, y1, x2, y2)
            y1 += CELL_SIZE
            y2 += CELL_SIZE

        # Вертикальные линии
        x1 = x2 = self.INDENT
        y1 = self.INDENT
        y2 = CELL_SIZE * self.board.ROWS + self.INDENT
        for i in range(self.board.COLS + 1):
            painter.drawLine(x1, y1, x2, y2)
            x1 += CELL_SIZE
            x2 += CELL_SIZE

    @painter_context
    def _draw_current_piece(self, painter: QPainter):
        if not self.current_piece:
            return

        for x, y in self.current_piece.get_points():
            draw_cell_board(
                painter,
                x,
                y,
                self.current_piece.get_color(),
                indent=self.INDENT,
            )

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

                draw_cell_board(painter, x, y, color, indent=self.INDENT)

    @painter_context
    def _draw_glass(self, painter: QPainter):
        if self.timer.isActive():
            return

        text = "PAUSE"

        # Алгоритм изменения размера текста взят из http://stackoverflow.com/a/2204501
        # Для текущего пришлось немного адаптировать
        factor = min(self.width(), self.height()) / painter.fontMetrics().width(text)
        if factor < 1 or factor > 1.25:
            f = painter.font()
            point_size = f.pointSizeF() * factor
            if point_size > 0:
                f.setPointSizeF(point_size)
                painter.setFont(f)

        painter.setPen(Qt.black)

        brush = QColor(Qt.lightGray)
        brush.setAlphaF(0.6)

        painter.setBrush(brush)

        painter.drawRect(self.rect())
        painter.drawText(self.rect(), Qt.AlignCenter, text)

    def process_key(self, key: int):
        if key == Qt.Key_Space:
            if self.timer.isActive():
                self.timer.stop()
            else:
                self.timer.start()

            self.update()
            return

        if self.current_piece and self.timer.isActive():
            match key:
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

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self._draw_current_piece(painter)
        self._draw_shadow_of_current_piece(painter)
        self._draw_board(painter)
        self._draw_glass(painter)


class MainWindow(QWidget):
    TITLE: str = "Tetris"

    def __init__(self):
        super().__init__()

        self.next_piece_widget = PieceWidget()
        self.score_label = QLabel()

        self.board_widget = BoardWidget()
        self.board_widget.board.on_next_piece.connect(self.next_piece_widget.set_piece)
        self.board_widget.board.on_update_score.connect(self._update_states)
        self.board_widget.timer.timeout.connect(self._update_states)
        self.board_widget.on_finish.connect(
            lambda: QMessageBox.information(self, "Информация", "Проигрыш!")
        )

        def _add_button(text: str, key: Qt.Key) -> QToolButton:
            button = QToolButton()
            button.setText(text)
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.clicked.connect(lambda: self.board_widget.process_key(key))
            return button

        control_layout = QGridLayout()
        control_layout.addWidget(_add_button("🢁", Qt.Key_Up), 0, 1)
        control_layout.addWidget(_add_button("🢀", Qt.Key_Left), 1, 0)
        control_layout.addWidget(_add_button("🢂", Qt.Key_Right), 1, 2)
        control_layout.addWidget(_add_button("🢃", Qt.Key_Down), 2, 1)
        control_layout.addWidget(_add_button("Pause/Resume", Qt.Key_Space), 3, 0, 1, 4)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.next_piece_widget)
        right_layout.addWidget(self.score_label)
        right_layout.addLayout(control_layout)
        right_layout.addWidget(
            QLabel(
                """
                <table>
                    <tr><td>🢁 - Rotate</td><td>🢀 - Left</td></tr>
                    <tr><td>🢂 - Right</td><td>🢃 - Down</td></tr>
                </table>
                <p>Scores by rows:</p>
                <table>
                    <tr><td><b>1</b>: 100</td><td><b>2</b>: 300</td></tr>
                    <tr><td><b>3</b>: 700</td><td><b>4</b>: 1500</td></tr>
                </table>
                """
            )
        )
        right_layout.addStretch()

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.board_widget)
        main_layout.addLayout(right_layout)

        self.setFocus()

        self._update_states()

    def _update_states(self):
        score: int = self.board_widget.board.score

        self.setWindowTitle(
            f"{self.TITLE}. Score: {score}{'' if self.board_widget.timer.isActive() else '. Paused'}"
        )
        self.score_label.setText(f"Score: {score}")

    def keyReleaseEvent(self, event: QKeyEvent):
        self.board_widget.process_key(event.key())


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
