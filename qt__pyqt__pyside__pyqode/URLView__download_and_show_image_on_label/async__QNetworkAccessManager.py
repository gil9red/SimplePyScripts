#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


class URLView(Qt.QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        layout = Qt.QVBoxLayout(self)

        self.urlEdit = Qt.QLineEdit()
        self.urlEdit.setText("https://www.python.org/static/img/python-logo.png")
        layout.addWidget(self.urlEdit)

        self.imageLabel = Qt.QLabel("No image")
        self.imageLabel.setScaledContents(True)
        layout.addWidget(self.imageLabel)

        self.loadButton = Qt.QPushButton("Load")
        layout.addWidget(self.loadButton)

        self.loadButton.clicked.connect(self.on_load)

        self.nam = Qt.QNetworkAccessManager()
        self.nam.finished.connect(self.finish_request)

    def on_load(self) -> None:
        print("Load image")

        url = self.urlEdit.text()
        self.nam.get(Qt.QNetworkRequest(Qt.QUrl(url)))

    def finish_request(self, reply) -> None:
        img = Qt.QPixmap()
        img.loadFromData(reply.readAll())

        self.imageLabel.setPixmap(img)


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = URLView()
    w.show()
    app.exec()
