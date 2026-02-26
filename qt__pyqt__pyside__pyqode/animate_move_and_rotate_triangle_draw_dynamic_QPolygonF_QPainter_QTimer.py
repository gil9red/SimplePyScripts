#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import math

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QTransform, QPolygonF, QPen
from PyQt5.QtCore import QPointF, Qt, QTimer


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.angle = 0
        self.x = 0
        self.points = []

        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self._do_tick)
        self.timer.start()

    def _do_tick(self) -> None:
        self.angle += 5

        self.x += 5
        if self.x > self.width():
            self.x = 0
            self.points.clear()

        # Перерисование окна
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        height = 500
        y0 = height / 4
        amplitude = height / 2
        frequency = 0.04

        x = self.x
        y = y0 + math.sin(x * frequency) * amplitude / 2 + amplitude / 2

        triangle_points = [QPointF(0, 0), QPointF(0, 50), QPointF(50, 50)]
        for p in triangle_points:
            p.setX(p.x() + x)
            p.setY(p.y() + y)

        polygon = QPolygonF(triangle_points)

        center = polygon.boundingRect().center()
        self.points.append(center)

        painter.save()
        painter.setPen(QPen(Qt.red, 2))
        p1 = self.points[0]
        for p2 in self.points[1:]:
            painter.drawLine(p1, p2)
            p1 = p2
        painter.restore()

        transform = (
            QTransform()
            .translate(center.x(), center.y())
            .rotate(self.angle)
            .translate(-center.x(), -center.y())
        )

        p = transform.map(polygon)

        painter.setBrush(Qt.blue)
        painter.drawPolygon(p)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
