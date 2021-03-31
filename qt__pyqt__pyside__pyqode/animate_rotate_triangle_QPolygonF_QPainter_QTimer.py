#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QTransform, QPolygonF
from PyQt5.QtCore import QPointF, Qt, QTimer


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.angle = 0

        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self._do_tick)
        self.timer.start()

    def _do_tick(self):
        self.angle += 5

        # Перерисования окна
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        x, y = 100, 100

        painter.setBrush(Qt.blue)

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
