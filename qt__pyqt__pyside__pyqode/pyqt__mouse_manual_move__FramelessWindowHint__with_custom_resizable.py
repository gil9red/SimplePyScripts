#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback

from enum import Enum, auto

from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt


def log_uncaught_exceptions(ex_cls, ex, tb) -> None:
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)

    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


# Перечислить верхнюю левую, нижнюю правую и четыре неподвижные точки
class Direction(Enum):
    LEFT = auto()
    TOP = auto()
    RIGHT = auto()
    BOTTOM = auto()

    LEFT_TOP = auto()
    RIGHT_TOP = auto()
    LEFT_BOTTOM = auto()
    RIGHT_BOTTOM = auto()


class ResizableFramelessWidget(QWidget):
    # Четыре периметра
    MARGINS = 10

    def __init__(self) -> None:
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)

        self._old_pos = None
        self._direction = None
        self._is_margin_press = False

        # Отслеживание мыши
        self.setMouseTracking(True)

    def _is_left_top(self, pos):
        x_pos, y_pos = pos.x(), pos.y()
        return x_pos <= self.MARGINS and y_pos <= self.MARGINS

    def _is_right_bottom(self, pos):
        x_pos, y_pos = pos.x(), pos.y()
        wm, hm = self.width() - self.MARGINS, self.height() - self.MARGINS
        return wm <= x_pos <= self.width() and hm <= y_pos <= self.height()

    def _is_right_top(self, pos):
        x_pos, y_pos = pos.x(), pos.y()
        wm, hm = self.width() - self.MARGINS, self.height() - self.MARGINS
        return wm <= x_pos and y_pos <= self.MARGINS

    def _is_left_bottom(self, pos):
        x_pos, y_pos = pos.x(), pos.y()
        wm, hm = self.width() - self.MARGINS, self.height() - self.MARGINS
        return x_pos <= self.MARGINS and hm <= y_pos

    def _is_left(self, pos):
        x_pos, y_pos = pos.x(), pos.y()
        wm, hm = self.width() - self.MARGINS, self.height() - self.MARGINS
        return 0 <= x_pos <= self.MARGINS and self.MARGINS <= y_pos <= hm

    def _is_right(self, pos):
        x_pos, y_pos = pos.x(), pos.y()
        wm, hm = self.width() - self.MARGINS, self.height() - self.MARGINS
        return wm <= x_pos <= self.width() and self.MARGINS <= y_pos <= hm

    def _is_top(self, pos):
        x_pos, y_pos = pos.x(), pos.y()
        wm, hm = self.width() - self.MARGINS, self.height() - self.MARGINS
        return self.MARGINS <= x_pos <= wm and 0 <= y_pos <= self.MARGINS

    def _is_bottom(self, pos):
        x_pos, y_pos = pos.x(), pos.y()
        wm, hm = self.width() - self.MARGINS, self.height() - self.MARGINS
        return self.MARGINS <= x_pos <= wm and hm <= y_pos <= self.height()

    def mousePressEvent(self, event) -> None:
        """Событие клика мыши"""
        super().mousePressEvent(event)

        if event.button() == Qt.LeftButton:
            self._old_pos = event.pos()
            self._is_margin_press = False

            for func in (
                self._is_left_top,
                self._is_right_bottom,
                self._is_right_top,
                self._is_left_bottom,
                self._is_left,
                self._is_right,
                self._is_top,
                self._is_bottom,
            ):
                if func(self._old_pos):
                    self._is_margin_press = True
                    break

    def mouseReleaseEvent(self, event) -> None:
        """Событие отказов мыши"""
        super().mouseReleaseEvent(event)

        self._old_pos = None
        self._is_margin_press = False
        self._direction = None

    def mouseMoveEvent(self, event) -> None:
        """Событие перемещения мыши"""
        super().mouseMoveEvent(event)

        if self.isMaximized() or self.isFullScreen():
            self._direction = None
            self.setCursor(Qt.ArrowCursor)
            return

        pos = event.pos()

        # Если зажата кнопка мышки на границе виджета
        if self._old_pos and event.buttons() == Qt.LeftButton:
            if self._is_margin_press:
                self._resizeWidget(pos)
            else:
                # Для перемещения окна
                delta = pos - self._old_pos
                self.move(self.pos() + delta)

            return

        if self._is_left_top(pos):
            # Верхний левый угол
            self._direction = Direction.LEFT_TOP
            self.setCursor(Qt.SizeFDiagCursor)

        elif self._is_right_bottom(pos):
            # Нижний правый угол
            self._direction = Direction.RIGHT_BOTTOM
            self.setCursor(Qt.SizeFDiagCursor)

        elif self._is_right_top(pos):
            # верхний правый угол
            self._direction = Direction.RIGHT_TOP
            self.setCursor(Qt.SizeBDiagCursor)

        elif self._is_left_bottom(pos):
            # Нижний левый угол
            self._direction = Direction.LEFT_BOTTOM
            self.setCursor(Qt.SizeBDiagCursor)

        elif self._is_left(pos):
            # Влево
            self._direction = Direction.LEFT
            self.setCursor(Qt.SizeHorCursor)

        elif self._is_right(pos):
            # Право
            self._direction = Direction.RIGHT
            self.setCursor(Qt.SizeHorCursor)

        elif self._is_top(pos):
            # выше
            self._direction = Direction.TOP
            self.setCursor(Qt.SizeVerCursor)

        elif self._is_bottom(pos):
            # ниже
            self._direction = Direction.BOTTOM
            self.setCursor(Qt.SizeVerCursor)

        else:
            # Курсор по умолчанию
            self.setCursor(Qt.ArrowCursor)

    def _resizeWidget(self, pos) -> None:
        """Отрегулируйте размер окна"""
        if self._direction is None:
            return

        mpos = pos - self._old_pos
        x_pos, y_pos = mpos.x(), mpos.y()
        geometry = self.geometry()
        x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()

        if self._direction == Direction.LEFT_TOP:  # Верхний левый угол
            if w - x_pos > self.minimumWidth():
                x += x_pos
                w -= x_pos

            if h - y_pos > self.minimumHeight():
                y += y_pos
                h -= y_pos

        elif self._direction == Direction.RIGHT_BOTTOM:  # Нижний правый угол
            if w + x_pos > self.minimumWidth():
                w += x_pos
                self._old_pos = pos

            if h + y_pos > self.minimumHeight():
                h += y_pos
                self._old_pos = pos

        elif self._direction == Direction.RIGHT_TOP:  # верхний правый угол
            if h - y_pos > self.minimumHeight():
                y += y_pos
                h -= y_pos

            if w + x_pos > self.minimumWidth():
                w += x_pos
                self._old_pos.setX(pos.x())

        elif self._direction == Direction.LEFT_BOTTOM:  # Нижний левый угол
            if w - x_pos > self.minimumWidth():
                x += x_pos
                w -= x_pos

            if h + y_pos > self.minimumHeight():
                h += y_pos
                self._old_pos.setY(pos.y())

        elif self._direction == Direction.LEFT:  # Влево
            if w - x_pos > self.minimumWidth():
                x += x_pos
                w -= x_pos
            else:
                return

        elif self._direction == Direction.RIGHT:  # Право
            if w + x_pos > self.minimumWidth():
                w += x_pos
                self._old_pos = pos
            else:
                return

        elif self._direction == Direction.TOP:  # выше
            if h - y_pos > self.minimumHeight():
                y += y_pos
                h -= y_pos
            else:
                return

        elif self._direction == Direction.BOTTOM:  # ниже
            if h + y_pos > self.minimumHeight():
                h += y_pos
                self._old_pos = pos
            else:
                return

        self.setGeometry(x, y, w, h)


if __name__ == "__main__":
    app = QApplication([])

    w = ResizableFramelessWidget()

    layout = QVBoxLayout()
    layout.addStretch()
    layout.addWidget(QPushButton("Закрыть окно", clicked=w.close))

    w.setLayout(layout)
    w.resize(400, 400)
    w.show()

    app.exec()
