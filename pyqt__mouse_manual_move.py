#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.old_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.pos()

    def mouseMoveEvent(self, event):
        delta = event.pos() - self.old_pos
        self.move(self.pos() + delta)


if __name__ == '__main__':
    app = QApplication([])

    w = Widget()
    w.show()

    app.exec()
