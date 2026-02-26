#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QPixmap


class Label(QLabel):
    def __init__(self) -> None:
        super().__init__()

        self.pixmap = QPixmap("52rQ3.png")
        self.pixmap_leave = self.pixmap.copy(0, 0, 26, 26)
        self.pixmap_enter = self.pixmap.copy(26, 0, 52, 26)

        self.setPixmap(self.pixmap_leave)

    def enterEvent(self, event) -> None:
        self.setPixmap(self.pixmap_enter)

    def leaveEvent(self, event) -> None:
        self.setPixmap(self.pixmap_leave)


if __name__ == "__main__":
    app = QApplication([])

    mw = Label()
    mw.show()

    app.exec()
