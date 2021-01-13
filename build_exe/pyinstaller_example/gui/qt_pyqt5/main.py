#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget


app = QApplication(sys.argv)

line_edit = QLineEdit('New line')
button = QPushButton('Add')
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
w.setWindowTitle('Example')
w.setLayout(layout)
w.show()

app.exec_()
