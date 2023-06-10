#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from PyQt5 import Qt


class LoadUrlThread(Qt.QThread):
    load_finished = Qt.pyqtSignal(object)

    def __init__(self, url):
        super().__init__()

        self.url = url

    def run(self):
        rs = requests.get(self.url)
        self.load_finished.emit(rs)


class MainWindow(Qt.QMainWindow):
    def __init__(self):
        super().__init__()

        self.button = Qt.QPushButton("Load url!")
        self.button.clicked.connect(self.on_clicked)

        self.setCentralWidget(self.button)

    def on_finished_load_url(self, rs):
        self.setWindowTitle("After load: {}".format(rs))

    def on_clicked(self):
        url = "https://github.com/gil9red/SimplePyScripts"

        self.setWindowTitle("Before load")

        self.thread = LoadUrlThread(url)
        self.thread.load_finished.connect(self.on_finished_load_url)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()


if __name__ == "__main__":
    app = Qt.QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
