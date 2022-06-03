#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
import traceback

from typing import Optional

from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt5.QtGui import QPainter, QPaintEvent, QKeyEvent, QColor
from PyQt5.QtCore import Qt, QTimer

from config import DEBUG
from common import logger
from figure import Figure


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f'{ex_cls.__name__}: {ex}:\n'
    text += ''.join(traceback.format_tb(tb))

    logger.error(text)
    QMessageBox.critical(None, 'Error', text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class MainWindow(QWidget):
    ROWS = 20
    COLS = 10
    CELL_SIZE = 20
    SPEED_MS = 200

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Tetris')

        self.board_matrix: list[list[Optional[QColor]]] = [
            [None for _ in range(self.COLS)]
            for _ in range(self.ROWS)
        ]
        self.current_figure: Optional[Figure] = None
        self.next_figure: Optional[Figure] = None

        self.timer = QTimer()
        self.timer.timeout.connect(self._on_tick)
        self.timer.setInterval(self.SPEED_MS)
        self.timer.start()

    def abort_game(self):
        self.timer.stop()
        QMessageBox.information(self, "Информация", "Проигрыш!")

    def _on_logic(self):
        if not self.current_figure:
            if self.next_figure:
                self.current_figure = self.next_figure
            else:
                self.current_figure = Figure.get_random(
                    x=self.COLS // 2,  # По-умолчанию, по центру
                    y=0,
                    parent=self,
                )

            self.next_figure = Figure.get_random(
                x=self.COLS // 2,  # По-умолчанию, по центру
                y=0,
                parent=self,
            )

            # Если сразу после создания столкновение
            if self.current_figure.is_collapse():
                self.abort_game()

            return

        if not self.current_figure.move_down():
            self.current_figure.add_to_board()
            self.current_figure = None

            # TODO: В метод
            to_delete = []
            for row in reversed(self.board_matrix):
                if all(color for color in row):
                    to_delete.append(row)

            for row in to_delete:
                self.board_matrix.remove(row)
                self.board_matrix.insert(0, [None for _ in range(self.COLS)])

    def _on_tick(self):
        self._on_logic()
        self.update()

    def _draw_cell_board(self, painter: QPainter, x: int, y: int, color: QColor):
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        painter.drawRect(x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)

    def _draw_board(self, painter: QPainter):
        painter.save()

        # Рисование заполненных ячеек
        for y, row in enumerate(self.board_matrix):
            for x, cell_color in enumerate(row):
                if not cell_color:
                    continue

                self._draw_cell_board(painter, x, y, cell_color)

        painter.setPen(Qt.black)

        # Горизонтальные линии
        y1, y2 = 0, 0
        for i in range(self.ROWS + 1):
            painter.drawLine(0, y1, self.CELL_SIZE * self.COLS, y2)
            y1 += self.CELL_SIZE
            y2 += self.CELL_SIZE

        # Вертикальные линии
        x1, x2 = 0, 0
        for i in range(self.COLS + 1):
            painter.drawLine(x1, 0, x2, self.CELL_SIZE * self.ROWS)
            x1 += self.CELL_SIZE
            x2 += self.CELL_SIZE

        painter.restore()

    def _draw_current_figure(self, painter: QPainter):
        if not self.current_figure:
            return

        painter.save()

        for x, y in self.current_figure.get_points():
            self._draw_cell_board(painter, x, y, self.current_figure.get_color())

        # Рисуем центр фигуры
        if DEBUG:
            self._draw_cell_board(painter, self.current_figure.x, self.current_figure.y, Qt.black)

        x_next = self.COLS + 3
        y_next = 1
        for x, y in self.next_figure.get_points_for_state(x=x_next, y=y_next):
            self._draw_cell_board(painter, x, y, self.next_figure.get_color())

        painter.restore()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Рисование таблицы
        self._draw_board(painter)

        self._draw_current_figure(painter)

    def keyReleaseEvent(self, event: QKeyEvent):
        match event.key():
            case Qt.Key_Left if self.current_figure:
                if self.current_figure.move_left():
                    self.update()

            case Qt.Key_Right if self.current_figure:
                if self.current_figure.move_right():
                    self.update()

            case Qt.Key_Up if self.current_figure:
                if self.current_figure.turn_right():
                    self.update()

            case Qt.Key_Down if self.current_figure:
                while self.current_figure.move_down():
                    self.update()


if __name__ == '__main__':
    app = QApplication([])

    # from typing import Any
    #
    # from PyQt5.QtWidgets import QTableView
    # from PyQt5.QtCore import QAbstractTableModel, QModelIndex, QSize
    # from PyQt5.QtGui import QBrush
    #
    # class TetrisModel(QAbstractTableModel):
    #     ROWS = 20
    #     COLS = 10
    #     CELL_SIZE = 20 * 2
    #
    #     def rowCount(self, parent: QModelIndex = None) -> int:
    #         return self.ROWS
    #
    #     def columnCount(self, parent: QModelIndex = None) -> int:
    #         return self.COLS
    #
    #     def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
    #         if not index.isValid():
    #             return
    #
    #         match role:
    #             case Qt.BackgroundRole:
    #                 return QBrush(Qt.red)
    #
    #             case Qt.SizeHintRole:
    #                 return QSize(self.CELL_SIZE, self.CELL_SIZE)
    #
    #         # return super().data(index, role)
    #
    #     def flags(self, index: QModelIndex) -> Qt.ItemFlags:
    #         return Qt.ItemIsEnabled
    #
    #
    # view = QTableView()
    # view.setModel(TetrisModel())
    # view.resizeRowsToContents()
    # view.resizeColumnsToContents()
    # view.show()

    mw = MainWindow()
    mw.show()

    app.exec()
