#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


if __name__ == "__main__":
    import sys

    from PySide.QtGui import *

    # https://mborgerson.com/creating-an-executable-from-a-python-script

    app = QApplication(sys.argv)

    line_edit = QLineEdit("New line")
    button = QPushButton("Add")
    text_edit = QTextEdit()

    def add_to_text():
        text = line_edit.text()
        text_edit.append(text)

    button.clicked.connect(add_to_text)

    layout = QVBoxLayout()
    layout.addWidget(line_edit)
    layout.addWidget(button)
    layout.addWidget(text_edit)

    w = QWidget()
    w.setWindowTitle("Example")
    w.setLayout(layout)
    w.show()

    app.exec_()
