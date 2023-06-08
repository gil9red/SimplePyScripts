#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPainterPath, QTransform
from PyQt5.QtCore import QPointF, Qt, QRectF, QTimer


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

        rect = QRectF(0, 0, 50, 50)

        path = QPainterPath()
        path.moveTo(rect.left() + (rect.width() / 2), rect.top())
        path.lineTo(rect.bottomLeft())
        path.lineTo(rect.bottomRight())
        path.lineTo(rect.left() + (rect.width() / 2), rect.top())

        for i in range(path.elementCount()):
            point = QPointF(path.elementAt(i))
            point += QPointF(x, y)
            path.setElementPositionAt(i, point.x(), point.y())

        center = rect.center()
        transform = (
            QTransform()
            .translate(center.x() + x, center.y() + y)
            .rotate(self.angle)
            .translate(-center.x() - x, -center.y() - y)
        )

        path = transform.map(path)

        painter.fillPath(path, Qt.blue)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
