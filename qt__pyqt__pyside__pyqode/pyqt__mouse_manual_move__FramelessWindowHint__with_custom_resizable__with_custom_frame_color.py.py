#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen

from pyqt__mouse_manual_move__FramelessWindowHint__with_custom_resizable import (
    ResizableFramelessWidget,
)


class Widget(ResizableFramelessWidget):
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.frame_color = Qt.darkCyan

        layout = QVBoxLayout()
        layout.addWidget(
            QLabel("Перетаскиваем окно, созданное без полей.", alignment=Qt.AlignCenter)
        )
        layout.addWidget(QPushButton("Закрыть окно", clicked=self.close))

        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setBrush(Qt.white)
        painter.setPen(QPen(self.frame_color, self.MARGINS))

        painter.drawRect(self.rect())


if __name__ == "__main__":
    app = QApplication([])

    w = Widget()
    w.resize(400, 300)
    w.show()

    app.exec()
