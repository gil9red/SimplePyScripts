#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


class MainWindow(Qt.QMainWindow):
    def __init__(self):
        super().__init__()

        self.widget = Qt.QWidget()
        self.widget.resize(100, 100)

        button = Qt.QPushButton("Click!", clicked=self.show_and_move)

        self.setCentralWidget(button)

    def show_and_move(self):
        self.widget.hide()

        self.widget.move(self.geometry().center() - self.widget.rect().center())

        self.widget.show()


if __name__ == "__main__":
    app = Qt.QApplication([])

    mw = MainWindow()
    mw.resize(500, 500)
    mw.show()

    app.exec()
