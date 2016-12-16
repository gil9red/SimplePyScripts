#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


text = 'titan'
url = 'http://gama-gama.ru/search/?searchField=' + text

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


app = QApplication([])

view = QWebEngineView()
view.show()

view.load(QUrl(url))

app.exec()
