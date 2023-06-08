#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib import request
from PyQt5 import Qt


class URLView(Qt.QWidget):
    def __init__(self, parent=None):
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

    def on_load(self):
        print("Load image")

        url = self.urlEdit.text()
        data = request.urlopen(url).read()
        pixmap = Qt.QPixmap()
        pixmap.loadFromData(data)
        self.imageLabel.setPixmap(pixmap)


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = URLView()
    w.show()
    app.exec()
