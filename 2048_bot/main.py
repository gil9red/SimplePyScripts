# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    import sys

    try:
        from PyQt4.QtGui import QApplication
    except ImportError:
        from PySide.QtGui import QApplication

    from mainwindow import MainWindow

    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.resize(1400, 800)
    mw.read_settings()
    mw.show()

    sys.exit(app.exec_())
