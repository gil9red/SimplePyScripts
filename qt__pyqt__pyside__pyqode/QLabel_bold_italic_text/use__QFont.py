#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.Qt import QApplication, QLabel, QVBoxLayout, QWidget


app = QApplication([])

label_1 = QLabel()
label_1.setText("Hello World!!!")

font = label_1.font()
font.setItalic(True)
font.setBold(True)
label_1.setFont(font)

label_2 = QLabel()
label_2.setText("nothing...")

layout = QVBoxLayout()
layout.addWidget(label_1)
layout.addWidget(label_2)

mw = QWidget()
mw.setLayout(layout)
mw.show()

app.exec()
