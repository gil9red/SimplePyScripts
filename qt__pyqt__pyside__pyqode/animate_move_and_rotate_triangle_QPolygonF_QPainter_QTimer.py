#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import math

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QTransform, QPolygonF, QPen
from PyQt5.QtCore import QPointF, Qt, QTimer


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.angle = 0
        self.x = 0
        self.S = 0

        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self._do_tick)
        self.timer.start()

    def _do_tick(self):
        self.angle += 5
        self.x += 5

        if self.x > self.width():
            self.x = 0

        # Перерисования окна
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        y0 = self.height() / 4
        amplitude = self.height() / 2
        frequency = .01

        painter.save()
        painter.setPen(QPen(Qt.black, 2))
        for x in range(self.width()):
            y = y0 + math.sin(x * frequency) * amplitude / 2 + amplitude / 2
            painter.drawPoint(x, y)
        painter.restore()

        painter.setBrush(Qt.blue)

        x = self.x
        y = y0 + math.sin(x * frequency) * amplitude / 2 + amplitude / 2

        triangle_points = [
            QPointF(0, 0), QPointF(0, 50), QPointF(50, 50)
        ]
        for p in triangle_points:
            p.setX(p.x() + x)
            p.setY(p.y() + y)

        p = QPolygonF(triangle_points)

        center = p.boundingRect().center()
        transform = QTransform() \
            .translate(center.x(), center.y())\
            .rotate(self.angle)\
            .translate(-center.x(), -center.y())

        p = transform.map(p)
        painter.drawPolygon(p)


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
