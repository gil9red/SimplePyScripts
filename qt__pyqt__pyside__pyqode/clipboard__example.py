#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QLabel,
    QPushButton,
    QMessageBox,
)
from PyQt5.QtCore import Qt


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = "{}: {}:\n".format(ex_cls.__name__, ex)
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        layout = QGridLayout()

        items = ['0.3"', '1"', '0.56"', '0.25"', '0.58"', '0.81"', '0.75"', '3.25"']

        for i, x in enumerate(items, 1):
            button = QPushButton(x)
            button.clicked.connect(lambda ok, x=x: QApplication.clipboard().setText(x))

            layout.addWidget(QLabel(f"#{i}"), 0, i, Qt.AlignHCenter)
            layout.addWidget(button, 1, i)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
