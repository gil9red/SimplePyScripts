#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView


app = QApplication([])

view = QWebEngineView()
view.show()

url = "https://www.google.com/search?q=hello world"
view.load(QUrl(url))

app.exec()
