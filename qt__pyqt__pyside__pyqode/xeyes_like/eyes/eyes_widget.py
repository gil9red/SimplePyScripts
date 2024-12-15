#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QCursor, QResizeEvent
from PyQt5.QtCore import QTimer, QPoint

from .eye_widget import EyeWidget


D_INDENT_TOP = 20
D_INDENT_LEFT = 4
D_INDENT_RIGHT = 4
D_INDENT_BOTTOM = 4
D_INDENT_BETWEEN_EYES = 1


class EyesWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.eyes: list[EyeWidget] = [EyeWidget(self) for _ in range(2)]

        self.timerCursorPos = QTimer(self)
        self.timerCursorPos.timeout.connect(self.refresh_look_there)
        self.timerCursorPos.start(30)

    def refresh_look_there(self):
        self.update()

        position: QPoint = QCursor.pos()
        for eye in self.eyes:
            eye.look_there(position)

    def update_minimum_size(self):
        if not self.eyes:
            return

        width_eye: int = self.eyes[0].width()
        height_eye: int = self.eyes[0].height()

        sum_indent: int = (len(self.eyes) - 1) * D_INDENT_BETWEEN_EYES

        sum_width_eyes: int = len(self.eyes) * width_eye

        min_width = sum_width_eyes + D_INDENT_LEFT + D_INDENT_RIGHT + sum_indent
        min_height = height_eye + D_INDENT_TOP + D_INDENT_BOTTOM

        self.setMinimumSize(
            min_width + D_INDENT_LEFT + D_INDENT_RIGHT,
            min_height + D_INDENT_TOP + D_INDENT_BOTTOM,
        )

    def update_size(self):
        self.update_minimum_size()
        QApplication.instance().postEvent(self, QResizeEvent(self.size(), self.size()))

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)

        if not self.eyes:
            return

        x: int = D_INDENT_LEFT
        y: int = D_INDENT_RIGHT

        w = (
            event.size().width()
            - (D_INDENT_LEFT + D_INDENT_RIGHT)
            - (len(self.eyes) - 1) * D_INDENT_BETWEEN_EYES
        ) / len(self.eyes)
        h = event.size().height() - (D_INDENT_TOP + D_INDENT_BOTTOM)

        diameter: int = int(min(w, h))

        for eye in self.eyes:
            eye.move(x, y)
            eye.setFixedSize(diameter, diameter)

            x = eye.x() + eye.width() + D_INDENT_BETWEEN_EYES
