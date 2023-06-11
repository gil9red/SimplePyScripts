#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback

from PyQt5.QtWidgets import QMessageBox, QWidget, QApplication
from PyQt5.QtGui import QMouseEvent, QPaintEvent, QPainter, QColor
from PyQt5.QtCore import Qt


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = "{}: {}:\n".format(ex_cls.__name__, ex)
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.pos = None
        self.pos_list = []

    def mousePressEvent(self, event: QMouseEvent):
        self.pos = event.pos()

        self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        self.pos = event.pos()

        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.pos_list.append(self.pos)
        self.pos = None

        self.update()

    def paintEvent(self, event: QPaintEvent):
        if not self.pos and not self.pos_list:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#AAFF0000"))

        for pos in self.pos_list:
            painter.drawEllipse(pos, 40, 40)

        if self.pos:
            painter.drawEllipse(self.pos, 40, 40)


if __name__ == "__main__":
    app = QApplication([])

    w = Widget()
    w.show()

    app.exec()
