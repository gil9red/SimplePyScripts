#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import traceback
import sys

from PyQt5.QtWidgets import QApplication, QMessageBox

from eyes.eyes_widget import EyesWidget
# TODO:
# from support import set_top_of_all_windows


def log_uncaught_exceptions(ex_cls, ex, tb) -> None:
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


app = QApplication([])
app.setApplicationName("Eyes")

w = EyesWidget()
w.resize(200, 100)
w.move(100, 100)
w.show()
w.update_size()

# TODO: On closing EyesWidget needs to finish of QApplication
# set_top_of_all_windows(w, True)

app.exec()
