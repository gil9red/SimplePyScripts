#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "ipetrash"


from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsLinearLayout,
    QGraphicsWidget,
)
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt


class Window(QGraphicsView):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("loading_gif")
        self.resize(250, 120)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        main_layout = QGraphicsLinearLayout(Qt.Horizontal)

        form = QGraphicsWidget()
        form.setLayout(main_layout)

        self.scene.addItem(form)

        for i in range(3):
            movie = QMovie("loading.gif")
            label_loading = QLabel()
            label_loading.setMovie(movie)
            movie.start()

            label_loading.setFrameStyle(QLabel.Box)
            label_loading.setAttribute(Qt.WA_OpaquePaintEvent)

            proxy_item = self.scene.addWidget(label_loading)
            main_layout.addItem(proxy_item)


if __name__ == "__main__":
    app = QApplication([])

    mw_1 = Window()
    mw_1.show()

    mw_2 = Window()
    mw_2.setStyleSheet("background-color: green")
    mw_2.show()

    app.exec()
