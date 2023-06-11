#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QLabel, QApplication, QGridLayout, QWidget
from PyQt5.QtCore import Qt


def create_label(alignment):
    label = QLabel("Test")
    label.setFixedSize(40, 40)
    label.setFrameStyle(QLabel.Box)
    label.setAlignment(alignment)

    return label


app = QApplication([])

layout = QGridLayout()
layout.addWidget(create_label(Qt.AlignLeft), 0, 0)
layout.addWidget(create_label(Qt.AlignLeft | Qt.AlignBottom), 0, 1)
layout.addWidget(create_label(Qt.AlignLeft | Qt.AlignVCenter), 0, 2)
layout.addWidget(create_label(Qt.AlignLeft | Qt.AlignTop), 0, 3)
layout.addWidget(create_label(Qt.AlignHCenter | Qt.AlignTop), 0, 4)
layout.addWidget(create_label(Qt.AlignRight | Qt.AlignVCenter), 0, 5)

w = QWidget()
w.setLayout(layout)
w.show()

app.exec()
