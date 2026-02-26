#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "ipetrash"


from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QLabel
from PyQt5.QtGui import QMovie


class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("loading_gif")

        self.main_layout = QHBoxLayout()

        for i in range(3):
            movie = QMovie("loading.gif")
            label_loading = QLabel()
            label_loading.setMovie(movie)
            movie.start()

            label_loading.setFrameStyle(QLabel.Box)

            self.main_layout.addWidget(label_loading)

        self.setLayout(self.main_layout)


if __name__ == "__main__":
    app = QApplication([])

    mw_1 = Window()
    mw_1.show()

    mw_2 = Window()
    mw_2.setStyleSheet("background-color: green")
    mw_2.show()

    app.exec()
