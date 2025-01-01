#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback
from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGridLayout,
    QToolButton,
    QPushButton,
    QScrollArea,
)

from src.core.common import logger, seconds_to_str
from src.gui.common import StatusGameEnum
from src.gui.board_widget import BoardWidget
from src.gui.piece_widget import PieceWidget


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    logger.error(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


# SOURCE: https://github.com/gil9red/parse_jira_logged_time/blob/9a842ed071f317b7323b7b7775aa9f5195dbaf47/widgets/__init__.py#L218
def get_scroll_area(widget: QWidget) -> QScrollArea:
    scroll_area = QScrollArea()
    scroll_area.setFrameStyle(QScrollArea.NoFrame)
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(widget)

    return scroll_area


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


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/0360c558f85c0fe5e7320d88f90c0a4e23a7e342/seconds_to_str.py
def seconds_to_str(seconds: int | float) -> str:
    hh, mm = divmod(seconds, 3600)
    mm, ss = divmod(mm, 60)
    return "%02d:%02d:%02d" % (hh, mm, ss)


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


class StatusGameEnum(enum.IntEnum):
    INITED = enum.auto()
    STARTED = enum.auto()
    PAUSED = enum.auto()
    FINISHED = enum.auto()


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

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def minimumSizeHint(self) -> QSize:
        columns = self.board.COLS
        width = (CELL_SIZE * columns) + (self.INDENT * 2)

        rows = self.board.ROWS
        height = (CELL_SIZE * rows) + (self.INDENT * 2)
        return QSize(width, height)

    def heightForWidth(self, w: int) -> int:
        columns = self.board.COLS
        rows = self.board.ROWS

        return w * columns // rows

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


class MainWindow(QWidget):
    TITLE: str = "Tetris"

    def __init__(self):
        super().__init__()

        self.next_piece_widget = PieceWidget()
        self.score_label = QLabel()
        self.playing_time_label = QLabel()

        self.board_widget = BoardWidget()
        self.board_widget.board.on_next_piece.connect(self.next_piece_widget.set_piece)
        self.board_widget.board.on_update_score.connect(self._update_states)
        self.board_widget.on_tick.connect(self._update_states)
        self.board_widget.on_finish.connect(self._update_states)

        def _add_button(text: str, key: Qt.Key) -> QToolButton:
            button = QToolButton()
            button.setText(text)
            button.clicked.connect(lambda: self.board_widget.process_key(key))
            return button

        self.up_button = _add_button("🢁", Qt.Key_Up)
        self.left_button = _add_button("🢀", Qt.Key_Left)
        self.right_button = _add_button("🢂", Qt.Key_Right)
        self.down_button = _add_button("🢃", Qt.Key_Down)
        self.pause_resume_button = _add_button("Pause/Resume", Qt.Key_Space)

        control_layout = QGridLayout()
        control_layout.addWidget(self.up_button, 0, 1)
        control_layout.addWidget(self.left_button, 1, 0)
        control_layout.addWidget(self.right_button, 1, 2)
        control_layout.addWidget(self.down_button, 2, 1)
        control_layout.addWidget(self.pause_resume_button, 3, 0, 1, 4)

        self.start_button = QPushButton("START")
        self.start_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.start_button.clicked.connect(
            lambda: self.board_widget.process_key(Qt.Key_Return)
        )

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.next_piece_widget)
        right_layout.addWidget(self.score_label)
        right_layout.addWidget(self.playing_time_label)
        right_layout.addWidget(self.start_button)
        right_layout.addLayout(control_layout)
        right_layout.addWidget(
            QLabel(
                """
                <table>
                    <tr><td colspan="2">ENTER - Start</td></tr>
                    <tr><td colspan="2">SPACE - Pause/Resume</td></tr>
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

        widget_right = QWidget()
        widget_right.setLayout(right_layout)

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.board_widget, stretch=1)
        main_layout.addWidget(get_scroll_area(widget_right))

        for w in self.findChildren(QWidget):
            if isinstance(w, BoardWidget):
                continue

            w.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self._update_states()

    def _update_states(self):
        score: int = self.board_widget.board.score
        playing_time = seconds_to_str(self.board_widget.playing_time_ms // 1000)

        title_parts = [self.TITLE]

        if self.board_widget.status != StatusGameEnum.INITED:
            title_parts.append(f"Score: {score}")
            title_parts.append(f"Time: {playing_time}")

        if self.board_widget.status == StatusGameEnum.PAUSED:
            title_parts.append("Paused")

        self.setWindowTitle(". ".join(title_parts))
        self.score_label.setText(f"Score: {score}")
        self.playing_time_label.setText(f"Time: {playing_time}")

        self.start_button.setEnabled(
            self.board_widget.status in [StatusGameEnum.INITED, StatusGameEnum.FINISHED]
        )

        is_started = self.board_widget.status == StatusGameEnum.STARTED
        self.up_button.setEnabled(is_started)
        self.left_button.setEnabled(is_started)
        self.right_button.setEnabled(is_started)
        self.down_button.setEnabled(is_started)

        self.pause_resume_button.setEnabled(
            is_started or self.board_widget.status == StatusGameEnum.PAUSED
        )

    def keyReleaseEvent(self, event: QKeyEvent):
        self.board_widget.process_key(event.key())
        self._update_states()


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    # mw = QWidget()
    # main_layout = QHBoxLayout(mw)
    #
    # for cls in Piece.__subclasses__():
    #     piece_widget = PieceWidget()
    #     piece_widget.set_piece(cls(0, 0))
    #     main_layout.addWidget(piece_widget)
    #
    # mw.show()

    app.exec()
