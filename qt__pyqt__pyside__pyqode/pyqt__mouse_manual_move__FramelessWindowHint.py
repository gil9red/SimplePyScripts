#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)

        self._old_pos = None

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(QPushButton("Закрыть окно", clicked=self.close))

        self.setLayout(layout)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self._old_pos = event.pos()

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self._old_pos = None

    def mouseMoveEvent(self, event) -> None:
        if not self._old_pos:
            return

        delta = event.pos() - self._old_pos
        self.move(self.pos() + delta)


if __name__ == "__main__":
    app = QApplication([])

    w = Widget()
    w.resize(400, 400)
    w.show()

    app.exec()
