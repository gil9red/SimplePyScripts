#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from _test_widget import MainWindow


app = QApplication(sys.argv)

# SOURCE: https://codemyui.com/git-kraken-inspired-rotate-loading-animation/
splash = QSplashScreen(QPixmap("rotate-pulsating-loading-animation.gif"))
splash.show()

splash.showMessage(
    "Ожидание создания интерфейса", Qt.AlignHCenter | Qt.AlignBottom, Qt.white
)
w = MainWindow()

splash.showMessage(
    "Ожидание загрузки данных", Qt.AlignHCenter | Qt.AlignBottom, Qt.white
)
w.do_load()

w.show()

splash.finish(w)

sys.exit(app.exec())
