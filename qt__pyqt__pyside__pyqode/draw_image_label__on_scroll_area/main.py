#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback

from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QLabel,
    QHBoxLayout,
    QScrollArea,
    QMessageBox,
)
from PyQt5.QtGui import QPainter, QColor, QPixmap, QPalette
from PyQt5.QtCore import Qt, QEvent


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = "{}: {}:\n".format(ex_cls.__name__, ex)
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.flag = False

        self.image = QPixmap("image.jpg")

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignLeft)
        self.label.setPixmap(self.image)

        # Установка фильтра событий
        self.label.installEventFilter(self)

        self.scroll_area = QScrollArea()
        self.scroll_area.setBackgroundRole(QPalette.Dark)
        self.scroll_area.setWidget(self.label)

        layout = QHBoxLayout()
        layout.addWidget(self.scroll_area)
        self.setLayout(layout)

        # Рисовать будем на картинке
        self.painter = QPainter(self.image)
        self.painter.setBrush(QColor("yellow"))

    def eventFilter(self, obj, e):
        # Если событие пришло от self.label
        if obj == self.label:
            # Если событие нажатия кнопки мышки и зажата левая кнопка
            if e.type() == QEvent.MouseButtonPress and e.button() == Qt.LeftButton:
                self.flag = True
                self.draw_ellipse(e)

            # Если событие отпускания кнопки мышки и зажата левая кнопка
            elif e.type() == QEvent.MouseButtonRelease and e.button() == Qt.LeftButton:
                self.flag = False

            # Если событие движения мышки и зажата левая кнопка
            elif e.type() == QEvent.MouseMove and self.flag:
                self.draw_ellipse(e)

        # Стандартная обработка событий
        return super().eventFilter(obj, e)

    def draw_ellipse(self, e):
        self.painter.drawEllipse(e.pos(), 20, 20)
        self.label.setPixmap(self.image)


if __name__ == "__main__":
    app = QApplication([])

    w = Example()
    w.resize(500, 500)
    w.show()

    app.exec()
