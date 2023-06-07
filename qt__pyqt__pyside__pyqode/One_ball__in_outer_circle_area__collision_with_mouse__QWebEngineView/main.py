#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.stackoverflow.com/a/970882/201445


from pathlib import Path

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView


if __name__ == "__main__":
    with open("index.html", encoding="utf-8") as f:
        html = f.read()

    title = Path(__file__).parent.name

    app = QApplication([])

    view = QWebEngineView()
    view.setWindowTitle(title)
    view.setHtml(html)
    view.show()

    app.exec()
