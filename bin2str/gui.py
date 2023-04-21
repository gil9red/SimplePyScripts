#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import traceback
import sys

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *

except:
    try:
        from PyQt4.QtGui import *
        from PyQt4.QtCore import *

    except:
        from PySide.QtGui import *
        from PySide.QtCore import *


from bin2str import bin2str, str2bin


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("bin2str")

        button_bin2str = QPushButton("bin -> str")
        button_bin2str.clicked.connect(self._bin2str)

        button_str2bin = QPushButton("str -> bin")
        button_str2bin.clicked.connect(self._str2bin)

        self.plain_text_bin = QPlainTextEdit()
        self.plain_text_str = QPlainTextEdit()

        h_layout = QHBoxLayout()
        h_layout.addWidget(button_bin2str)
        h_layout.addWidget(button_str2bin)

        layout = QVBoxLayout()
        layout.addLayout(h_layout)
        layout.addWidget(QLabel("Bin:"))
        layout.addWidget(self.plain_text_bin)
        layout.addSpacing(10)
        layout.addWidget(QLabel("Text:"))
        layout.addWidget(self.plain_text_str)

        self.setLayout(layout)

    def _bin2str(self):
        text = self.plain_text_bin.toPlainText()
        text = bin2str(text)

        self.plain_text_str.setPlainText(text)

    def _str2bin(self):
        text = self.plain_text_str.toPlainText()
        text = str2bin(text)

        self.plain_text_bin.setPlainText(text)


if __name__ == "__main__":
    app = QApplication([])

    w = Widget()
    w.plain_text_bin.setPlainText(
        "01001000 01100101 01101100 01101100 01101111 00100000 "
        "01010111 01101111 01110010 01101100 01100100 00100001"
    )
    w.show()

    app.exec()
