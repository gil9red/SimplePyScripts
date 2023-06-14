#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Пример получения и сохранения стандартной иконки Qt в base64.

Немного изменив, можно и сохранять их.

"""


import base64
import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


# Для отлова всех исключений, которые в слотах Qt могут "затеряться" и привести к тихому падению
def log_uncaught_exceptions(ex_cls, ex, tb):
    text = "{}: {}:\n".format(ex_cls.__name__, ex)
    text += "".join(traceback.format_tb(tb))

    print("Error: ", text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


app = QApplication([])

style = QWidget().style()
clear_icon = style.standardIcon(QStyle.SP_LineEditClearButton)

print(clear_icon.availableSizes())

for size in clear_icon.availableSizes():
    pixmap = clear_icon.pixmap(size)

    bytes = QByteArray()
    buffer = QBuffer(bytes)
    buffer.open(QIODevice.WriteOnly)
    pixmap.save(buffer, "PNG")

    print(size, base64.b64encode(bytes))
