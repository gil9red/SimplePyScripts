#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import traceback
import sys

from PyQt5.QtWidgets import QApplication, QMessageBox

from eyes_widget import UEyesWidget


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f'{ex_cls.__name__}: {ex}:\n'
    text += ''.join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, 'Error', text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


app = QApplication([])
app.setApplicationName("Eyes")
# app.setApplicationVersion("0.0.1")
# app.setQuitOnLastWindowClosed(False)


# TODO:
w = UEyesWidget()
# w.setNumberEyes(2)
# w.setOrientation(Qt::Horizontal)
# w.setOpacity(0.6)
# w.setBrush(Qt::black)
w.resize(200, 100)
w.move(100, 100)
w.show()
# w.showFrame()
w.updateSize()

app.exec()
