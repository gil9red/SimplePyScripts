#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
from PyQt5.QtWidgets import QMessageBox


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, 'Error', text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QPushButton

    app = QApplication([])

    button = QPushButton("DON'T PUSH ME!")
    button.resize(200, 200)
    button.clicked.connect(lambda: 1 / 0)
    button.show()

    app.exec()
