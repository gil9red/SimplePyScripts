#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._old_pos = None
        self.frame_color = Qt.darkCyan

        layout = QVBoxLayout()
        layout.addWidget(
            QLabel("Перетаскиваем окно, созданное без полей.", alignment=Qt.AlignCenter)
        )
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

    def enterEvent(self, event) -> None:
        self.frame_color = Qt.darkCyan

        self.update()

    def leaveEvent(self, event) -> None:
        self.frame_color = Qt.darkGreen

        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)

        painter.setBrush(Qt.white)
        painter.setPen(QPen(self.frame_color, 20))

        painter.drawRect(self.rect())


if __name__ == "__main__":
    app = QApplication([])

    w = Widget()
    w.resize(400, 300)
    w.show()

    app.exec()
