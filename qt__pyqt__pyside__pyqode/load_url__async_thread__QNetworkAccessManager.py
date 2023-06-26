#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


class MainWindow(Qt.QMainWindow):
    def __init__(self):
        super().__init__()

        self.button = Qt.QPushButton("Load url!")
        self.button.clicked.connect(self.on_clicked)

        self.manager = Qt.QNetworkAccessManager(self)
        self.manager.finished.connect(self.on_reply_finished)

        self.setCentralWidget(self.button)

    def on_reply_finished(self, reply):
        self.setWindowTitle(f"After load: {reply}")

    def on_clicked(self):
        url = "https://github.com/gil9red/SimplePyScripts"

        self.setWindowTitle("Before load")

        # Отправляем запрос
        self.manager.get(Qt.QNetworkRequest(Qt.QUrl(url)))


if __name__ == "__main__":
    app = Qt.QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
