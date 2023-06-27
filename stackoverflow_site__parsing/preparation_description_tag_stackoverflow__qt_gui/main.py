#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


if __name__ == "__main__":
    import sys
    from PySide.QtGui import QApplication
    from mainwindow import MainWindow

    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.read_settings()
    mw.show()

    mw.fill_tag_list()

    sys.exit(app.exec_())
