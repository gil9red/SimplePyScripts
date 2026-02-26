#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.stackoverflow.com/a/1355594/201445


import sys

from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import (
    Qt,
    QEasingCurve,
    QPropertyAnimation,
    pyqtProperty,
    QPoint,
    QRect,
)


class ToggleButton(QCheckBox):
    def __init__(
        self,
        width=70,
        height=40,
        bg_color="#777",
        circle_color="#DDD",
        active_color="#00BCff",
        animation_curve=QEasingCurve.OutBounce,
    ) -> None:
        super().__init__()

        self.setFixedSize(width, height)
        self.setCursor(Qt.PointingHandCursor)

        self._bg_color = bg_color
        self._circle_color = circle_color
        self._active_color = active_color

        self._circle_margin = 3
        self._circle_position = self._circle_margin
        self._circle_size = self.height() - self._circle_margin

        self.animation = QPropertyAnimation(self, b"circle_position")
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(500)
        self.stateChanged.connect(self.start_transition)

    @pyqtProperty(int)
    def circle_position(self) -> int:
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos: int) -> None:
        self._circle_position = pos
        self.update()

    def start_transition(self, value) -> None:
        self.animation.setStartValue(self.circle_position)
        if value:
            self.animation.setEndValue(self.width() - self._circle_size)
        else:
            self.animation.setEndValue(self._circle_margin)
        self.animation.start()

    def hitButton(self, pos: QPoint) -> bool:
        return self.contentsRect().contains(pos)

    def paintEvent(self, e) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(Qt.NoPen)

        rect = QRect(0, 0, self.width(), self.height())

        p.setBrush(QColor(self._active_color if self.isChecked() else self._bg_color))
        p.drawRoundedRect(
            0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2
        )

        p.setBrush(QColor(self._circle_color))

        x, y = self._circle_position, self._circle_margin
        p.drawEllipse(
            x,
            y,
            self._circle_size - self._circle_margin,
            self._circle_size - self._circle_margin,
        )


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

    class MainWindow(QWidget):
        def __init__(self) -> None:
            super().__init__()

            self.setWindowTitle("Анимация кнопки переключения")
            self.toggleBtn = ToggleButton()

            self.layout = QVBoxLayout(self)
            self.layout.addWidget(self.toggleBtn, Qt.AlignCenter, Qt.AlignCenter)

    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(500, 500)
    w.show()
    sys.exit(app.exec_())
