#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage


class Client(QWebEnginePage):
    def __init__(self, urls) -> None:
        self.app = QApplication([])

        super().__init__()

        self.response_list = []
        self.loadFinished.connect(self._on_load_finished)

        for url in urls:
            self.load(QUrl(url))
            self.app.exec_()

    def _on_load_finished(self) -> None:
        self.toHtml(self.callable)

    def callable(self, html_str) -> None:
        self.response_list.append(html_str)
        self.app.quit()


def go(urls):
    client = Client(urls)
    return client.response_list


if __name__ == "__main__":
    urls = [
        [
            "http://doc.qt.io/Qt-5/qwebenginepage.html",
            "https://yandex.ru/",
        ],
        [
            "http://doc.qt.io/Qt-5/qwebenginepage.html",
            "https://www.google.ru/",
        ],
        [
            "https://www.google.ru/",
        ],
    ]

    from multiprocessing import Pool

    with Pool() as p:
        results = p.map(go, urls)
        print(len(results))

    number = 1

    for result in results:
        print(len(result))

        for html in result:
            with open(f"result_{number}.html", "w", encoding="utf-8") as f:
                f.write(html)

            number += 1
