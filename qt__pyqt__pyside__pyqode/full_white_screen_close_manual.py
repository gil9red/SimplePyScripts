#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QApplication

from full_black_screen_close_manual import MainWindow


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow(background_color="white", text_color="black")
    mw.resize(600, 600)
    mw.showFullScreen()

    app.exec()
