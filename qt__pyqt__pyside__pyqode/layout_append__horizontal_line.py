#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5 import Qt


def get_horizontal_line():
    line = Qt.QFrame()
    line.setFrameShape(Qt.QFrame.HLine)
    line.setFrameShadow(Qt.QFrame.Sunken)
    line.setLineWidth(1)

    return line


app = Qt.QApplication([])

layout = Qt.QFormLayout()
layout.addRow('First', Qt.QLineEdit())
layout.addRow('Last', Qt.QLineEdit())
layout.addRow(get_horizontal_line())

layout.addRow('Phone', Qt.QLineEdit())
layout.addRow(get_horizontal_line())

layout.addRow('Ok?', Qt.QCheckBox())

mw = Qt.QWidget()
mw.setLayout(layout)
mw.show()

app.exec()
