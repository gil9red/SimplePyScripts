#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://ru.stackoverflow.com/a/970882/201445


from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView


if __name__ == '__main__':
    with open('index.html', encoding='utf-8') as f:
        html = f.read()

    app = QApplication([])

    view = QWebEngineView()
    view.setHtml(html)
    view.show()

    app.exec()

