#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsPixmapItem,
    QGraphicsTextItem,
)


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.scene = QGraphicsScene()
        self.scene.addItem(QGraphicsTextItem("loading..."))

        self.view = QGraphicsView()
        self.view.setScene(self.scene)

        self.nam = QNetworkAccessManager()
        self.nam.finished.connect(self.finish_request)

        url = "http://pp.vk.me/c627626/v627626428/be07/wbpWha0RqZ4.jpg"
        self.nam.get(QNetworkRequest(QUrl(url)))

        layout = QVBoxLayout()
        layout.addWidget(self.view)

        self.setLayout(layout)

    def finish_request(self, reply) -> None:
        self.scene.clear()

        img = QPixmap()
        img.loadFromData(reply.readAll())

        item = QGraphicsPixmapItem(img)
        self.scene.addItem(item)


if __name__ == "__main__":
    app = QApplication([])

    w = Widget()
    w.show()

    app.exec()
