#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"

from PyQt5.QtCore import pyqtSignal, QTimer, QSize, Qt
from PyQt5.QtGui import QPainter, QColor, QResizeEvent, QPaintEvent
from PyQt5.QtWidgets import QWidget, QSizePolicy

from ..core.board import Board
from ..core.common import seconds_to_str
from ..core.piece import Piece
from .common import CELL_SIZE, StatusGameEnum, painter_context, draw_cell_board


class BoardWidget(QWidget):
    INDENT: int = 1
    SPEED_MS: int = 400

    on_tick = pyqtSignal()
    on_finish = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.board = Board()

        self.cell_size: int = CELL_SIZE

        self.current_piece: Piece | None = None
        self.next_piece: Piece | None = None

        self.__timer = QTimer()
        self.__timer.timeout.connect(self._on_tick)
        self.__timer.setInterval(self.SPEED_MS)

        self.playing_time_ms: int = 0
        self.__status = StatusGameEnum.INITED

    def minimumSizeHint(self) -> QSize:
        columns = self.board.COLS
        width = (CELL_SIZE * columns) + (self.INDENT * 2)

        rows = self.board.ROWS
        height = (CELL_SIZE * rows) + (self.INDENT * 2)
        return QSize(width, height)

    @property
    def status(self) -> StatusGameEnum:
        return self.__status

    @status.setter
    def status(self, value: StatusGameEnum):
        if self.__status == value:
            return

        self.__status = value

        match value:
            case StatusGameEnum.INITED:
                self.__timer.stop()
                self.board.clear()
                self.playing_time_ms = 0

            case StatusGameEnum.STARTED:
                self.__timer.start()

            case StatusGameEnum.PAUSED:
                self.__timer.stop()

            case StatusGameEnum.FINISHED:
                self.__timer.stop()
                self.on_finish.emit()

    def abort_game(self):
        self.status = StatusGameEnum.FINISHED

    def _on_logic(self):
        if not self.board.do_step():
            self.abort_game()
            return

        self.current_piece = self.board.current_piece
        self.next_piece = self.board.next_piece

    def _on_tick(self):
        self._on_logic()

        self.update()

        self.playing_time_ms += self.__timer.interval()
        self.on_tick.emit()

    @painter_context
    def _draw_board(self, painter: QPainter):
        # Рисование заполненных ячеек
        for y, row in enumerate(self.board.matrix):
            for x, cell_color in enumerate(row):
                if not cell_color:
                    continue

                draw_cell_board(
                    painter,
                    x,
                    y,
                    cell_color,
                    cell_size=self.cell_size,
                    indent=self.INDENT,
                )

        painter.setPen(Qt.black)

        # Горизонтальные линии
        y1 = y2 = self.INDENT
        x1 = self.INDENT
        x2 = self.cell_size * self.board.COLS + self.INDENT
        for i in range(self.board.ROWS + 1):
            painter.drawLine(x1, y1, x2, y2)
            y1 += self.cell_size
            y2 += self.cell_size

        # Вертикальные линии
        x1 = x2 = self.INDENT
        y1 = self.INDENT
        y2 = self.cell_size * self.board.ROWS + self.INDENT
        for i in range(self.board.COLS + 1):
            painter.drawLine(x1, y1, x2, y2)
            x1 += self.cell_size
            x2 += self.cell_size

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
                cell_size=self.cell_size,
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

                draw_cell_board(
                    painter, x, y, color, cell_size=self.cell_size, indent=self.INDENT
                )

    @painter_context
    def _draw_glass(self, painter: QPainter):
        match self.status:
            case StatusGameEnum.INITED:
                text = "Press START"
            case StatusGameEnum.PAUSED:
                text = "PAUSE"
            case StatusGameEnum.FINISHED:
                playing_time = seconds_to_str(self.playing_time_ms // 1000)
                text = f"FINISHED\nScore: {self.board.score}\nTime: {playing_time}"
            case _:
                return

        # Алгоритм изменения размера текста взят из http://stackoverflow.com/a/2204501
        # Для текущего пришлось немного адаптировать
        max_line_width = max(
            painter.fontMetrics().width(line) for line in text.splitlines()
        )
        factor = min(self.width(), self.height()) / max_line_width
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
        if key == Qt.Key_Space and self.status in [
            StatusGameEnum.STARTED,
            StatusGameEnum.PAUSED,
        ]:
            if self.status == StatusGameEnum.STARTED:
                self.status = StatusGameEnum.PAUSED
            else:
                self.status = StatusGameEnum.STARTED

            self.update()
            return

        if key in [Qt.Key_Enter, Qt.Key_Return] and self.status in [
            StatusGameEnum.INITED,
            StatusGameEnum.FINISHED,
        ]:
            self.status = StatusGameEnum.INITED
            self.status = StatusGameEnum.STARTED
            self.update()
            return

        if self.current_piece and self.status == StatusGameEnum.STARTED:
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

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)

        w_aspect = event.size().width() // self.board.COLS
        h_aspect = event.size().height() // self.board.ROWS

        self.cell_size = min(w_aspect, h_aspect)

        self.update()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self._draw_current_piece(painter)
        self._draw_shadow_of_current_piece(painter)
        self._draw_board(painter)
        self._draw_glass(painter)
