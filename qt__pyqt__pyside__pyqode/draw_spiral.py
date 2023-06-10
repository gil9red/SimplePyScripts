#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://doc.qt.io/qt-5/qtopengl-2dpainting-example.html


from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import (
    QBrush,
    QFont,
    QPen,
    QPainter,
    QPaintEvent,
    QLinearGradient,
    QColor,
)
from PyQt5.QtCore import Qt, QPointF, QRectF, QTimer


class Helper:
    def __init__(self, is_reverse_rotation: bool, is_draw_all_spiral=False):
        super().__init__()

        self.is_reverse_rotation = is_reverse_rotation
        self.is_draw_all_spiral = is_draw_all_spiral

        gradient = QLinearGradient(QPointF(50, -20), QPointF(80, 20))
        gradient.setColorAt(0.0, Qt.white)
        gradient.setColorAt(1.0, QColor(0xA6, 0xCE, 0x39))

        self.background: QBrush = QBrush(QColor(64, 32, 64))

        self.circleBrush: QBrush = QBrush(gradient)

        self.circlePen: QPen = QPen(Qt.black)
        self.circlePen.setWidth(1)

        self.textFont: QFont = QFont()
        self.textFont.setPixelSize(50)

        self.textPen: QPen = QPen(Qt.white)

    def _draw_spiral(self, painter: QPainter, elapsed: int, is_reverse_rotation=False):
        r = elapsed / 1000.0
        n = 30

        painter.save()
        painter.setBrush(self.circleBrush)
        painter.setPen(self.circlePen)

        painter.rotate(elapsed * 0.030 * (-1 if is_reverse_rotation else 1))
        for i in range(n):
            painter.rotate(30 * (-1 if is_reverse_rotation else 1))
            factor = (i + r) / n
            radius = 0 + 120.0 * factor
            circleRadius = 1 + factor * 20
            painter.drawEllipse(
                QRectF(radius, -circleRadius, circleRadius * 2, circleRadius * 2)
            )

        painter.restore()

    def paint(self, painter: QPainter, event: QPaintEvent, elapsed: int):
        painter.fillRect(event.rect(), self.background)
        painter.translate(100, 100)

        self._draw_spiral(painter, elapsed, self.is_reverse_rotation)
        if self.is_draw_all_spiral:
            self._draw_spiral(painter, elapsed, not self.is_reverse_rotation)


class Widget(QWidget):
    def __init__(self, is_reverse_rotation: bool, is_draw_all_spiral=False):
        super().__init__()

        self.setFixedSize(200, 200)

        self.elapsed: int = 0
        self.helper = Helper(is_reverse_rotation, is_draw_all_spiral)

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(50)

    def animate(self):
        self.elapsed = (self.elapsed + self.timer.interval()) % 1000
        self.update()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.helper.paint(painter, event, self.elapsed)
        painter.end()


if __name__ == "__main__":
    from PyQt5.QtWidgets import QLabel, QHBoxLayout

    app = QApplication([])

    mw = QWidget()

    w1 = Widget(is_reverse_rotation=False)
    w2 = Widget(is_reverse_rotation=True)
    w3 = Widget(is_reverse_rotation=False, is_draw_all_spiral=True)

    layout = QHBoxLayout(mw)
    layout.addWidget(w1)
    layout.addWidget(QLabel("+"))
    layout.addWidget(w2)
    layout.addWidget(QLabel("="))
    layout.addWidget(w3)

    mw.show()

    app.exec()
