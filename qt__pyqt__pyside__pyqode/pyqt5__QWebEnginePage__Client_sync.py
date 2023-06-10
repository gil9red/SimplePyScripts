#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage


class Client(QWebEnginePage):
    def __init__(self, urls):
        self.app = QApplication([])

        super().__init__()

        self.response_list = []
        self.loadFinished.connect(self._on_load_finished)

        for url in urls:
            self.load(QUrl(url))
            self.app.exec_()

    def _on_load_finished(self):
        self.toHtml(self.callable)

    def callable(self, html_str):
        self.response_list.append(html_str)
        self.app.quit()


if __name__ == "__main__":
    urls = [
        "http://doc.qt.io/Qt-5/qwebenginepage.html",
        "https://www.google.ru/",
        "https://yandex.ru/",
    ]
    client = Client(urls)
    print(len(client.response_list), client.response_list)
    # 3 ['<!--?xml version="1.0" ...
