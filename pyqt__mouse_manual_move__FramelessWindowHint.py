#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)

        self.old_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.pos()

    def mouseMoveEvent(self, event):
        if not self.old_pos:
            return

        delta = event.pos() - self.old_pos
        self.move(self.pos() + delta)

    def mouseReleaseEvent(self, event):
        self.old_pos = None

if __name__ == '__main__':
    app = QApplication([])

    w = Widget()
    w.show()

    app.exec()
