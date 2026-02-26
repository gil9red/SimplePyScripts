#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QInputDialog,
    QMessageBox,
    QLabel,
    QLineEdit,
)


class Example(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Example")
        self.setCentralWidget(QLabel('<font size="100">Hello, <b>USER</b>!</font>'))


if __name__ == "__main__":
    app = QApplication([])

    password, ok = QInputDialog.getText(
        None, "Auth", "Input password:", QLineEdit.Password
    )
    if not ok:
        QMessageBox.warning(None, "Warning", "Need input password!")
        sys.exit()

    if password != "123":
        QMessageBox.warning(None, "Warning", "Invalid password!")
        sys.exit()

    w = Example()
    w.show()

    app.exec_()
