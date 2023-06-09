#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.lbl = QLabel("loading...")
        self.lbl.setAutoFillBackground(True)

        self.nam = QNetworkAccessManager()
        self.nam.finished.connect(self.finish_request)

        url = "http://pp.vk.me/c627626/v627626428/be07/wbpWha0RqZ4.jpg"
        self.nam.get(QNetworkRequest(QUrl(url)))

        layout = QVBoxLayout()
        layout.addWidget(self.lbl)

        self.setLayout(layout)

    def finish_request(self, reply):
        img = QPixmap()
        img.loadFromData(reply.readAll())

        self.lbl.setPixmap(img)


if __name__ == "__main__":
    app = QApplication([])

    w = Widget()
    w.show()

    app.exec()
