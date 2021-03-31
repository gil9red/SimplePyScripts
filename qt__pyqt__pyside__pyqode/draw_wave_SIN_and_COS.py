#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import math

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt


class MainWindow(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(Qt.black)
        painter.drawRect(self.rect())

        y0 = self.height() / 4
        amplitude = self.height() / 2
        frequency = .01

        painter.setPen(QPen(Qt.white, 2))
        for x in range(self.width()):
            y = y0 + amplitude / 2
            painter.drawPoint(x, y)

        painter.setPen(QPen(Qt.red, 2))
        for x in range(self.width()):
            y = y0 + math.sin(x * frequency) * amplitude / 2 + amplitude / 2
            painter.drawPoint(x, y)

        painter.setPen(QPen(Qt.green, 2))
        for x in range(self.width()):
            y = y0 + math.cos(x * frequency) * amplitude / 2 + amplitude / 2
            painter.drawPoint(x, y)


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
