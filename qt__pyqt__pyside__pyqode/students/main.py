#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

from PySide.QtGui import QApplication

from main_window import MyWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mw = MyWindow()
    mw.show()

    sys.exit(app.exec_())
