#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from ctypes import windll, c_int, byref

from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(QPushButton("Закрыть окно", clicked=self.close))

        self.setLayout(layout)

        windll.dwmapi.DwmExtendFrameIntoClientArea(
            c_int(self.winId()), byref(c_int(-1))
        )


if __name__ == "__main__":
    app = QApplication([])

    w = Widget()
    w.resize(400, 300)
    w.show()

    app.exec()
