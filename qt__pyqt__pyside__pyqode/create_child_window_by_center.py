#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QStyle
from PyQt5.QtCore import Qt, QPoint


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        pb_1 = QPushButton("Create [1]")
        pb_1.clicked.connect(self._create_new_window_1)

        pb_2 = QPushButton("Create [2]")
        pb_2.clicked.connect(self._create_new_window_2)

        pb_3 = QPushButton("Create [3]")
        pb_3.clicked.connect(self._create_new_window_3)

        pb_4 = QPushButton("Create [4]")
        pb_4.clicked.connect(self._create_new_window_4)

        layout = QVBoxLayout()
        layout.addWidget(pb_1)
        layout.addWidget(pb_2)
        layout.addWidget(pb_3)
        layout.addWidget(pb_4)
        layout.addStretch()

        self.setLayout(layout)

    def _create_new_window_1(self):
        widget = QWidget(self, flags=Qt.Window)
        widget.resize(200, 100)
        widget.show()

    def _create_new_window_2(self):
        widget = QWidget(self, flags=Qt.Window)
        widget.resize(200, 100)

        pos = self.geometry().center() - widget.rect().center()
        widget.move(pos)

        widget.show()

    def _create_new_window_3(self):
        widget = QWidget(self, flags=Qt.Window)
        widget.resize(200, 100)

        x = (self.geometry().width() - widget.width()) // 2
        y = (self.geometry().height() - widget.height()) // 2
        pos = self.mapToGlobal(QPoint(x, y))
        widget.move(pos)

        widget.show()

    def _create_new_window_4(self):
        widget = QWidget(self, flags=Qt.Window)
        widget.resize(200, 100)

        widget.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight, Qt.AlignCenter, widget.size(), self.geometry()
            )
        )
        widget.show()


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.resize(500, 400)
    mw.show()

    app.exec()
