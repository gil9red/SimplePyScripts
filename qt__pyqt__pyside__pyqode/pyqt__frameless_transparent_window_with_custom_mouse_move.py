#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPoint


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Example')
        self.setGeometry(300, 300, 300, 220)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.press = False
        self.last_pos = QPoint(0, 0)

    def mouseMoveEvent(self, event):
        if self.press:
            self.move(event.globalPos() - self.last_pos)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.press = True

        self.last_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.press = False

    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(Qt.black, 50))
        painter.drawRect(self.rect())


if __name__ == '__main__':
    app = QApplication([])

    w = Example()
    w.show()

    app.exec_()
