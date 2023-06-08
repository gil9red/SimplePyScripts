#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


app = QApplication([])

view = QWebEngineView()
view.show()

url = "http://gama-gama.ru/search/?searchField=titan"
view.load(QUrl(url))

view.loadFinished.connect(lambda x: view.grab().save("img.jpg"))

app.exec()
