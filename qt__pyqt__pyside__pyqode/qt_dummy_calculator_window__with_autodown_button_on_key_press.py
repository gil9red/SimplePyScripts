#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback

from PyQt5.QtWidgets import *


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = "{}: {}:\n".format(ex_cls.__name__, ex)
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("dummy_calculator_window")

        self.key_by_button = {i: QPushButton(i) for i in "0123456789"}

        layout = QGridLayout()
        layout.addWidget(self.key_by_button["7"], 0, 0)
        layout.addWidget(self.key_by_button["8"], 0, 1)
        layout.addWidget(self.key_by_button["9"], 0, 2)

        layout.addWidget(self.key_by_button["4"], 1, 0)
        layout.addWidget(self.key_by_button["5"], 1, 1)
        layout.addWidget(self.key_by_button["6"], 1, 2)

        layout.addWidget(self.key_by_button["1"], 2, 0)
        layout.addWidget(self.key_by_button["2"], 2, 1)
        layout.addWidget(self.key_by_button["3"], 2, 2)

        layout.addWidget(self.key_by_button["0"], 3, 0, 1, 3)

        self.setLayout(layout)

    def keyPressEvent(self, event):
        try:
            key = chr(event.key())

            if key in self.key_by_button:
                self.key_by_button[key].setDown(True)

        except:
            pass

        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        try:
            key = chr(event.key())

            if key in self.key_by_button:
                self.key_by_button[key].setDown(False)

        except:
            pass

        super().keyReleaseEvent(event)


if __name__ == "__main__":
    app = QApplication([])

    w = Widget()
    w.show()

    app.exec()
