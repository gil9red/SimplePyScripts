#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import QFrame


def get_horizontal_line():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setFrameShadow(QFrame.Sunken)
    line.setLineWidth(1)

    return line


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QFormLayout, QLineEdit, QCheckBox, QWidget

    app = QApplication([])

    layout = QFormLayout()
    layout.addRow('First', QLineEdit())
    layout.addRow('Last', QLineEdit())
    layout.addRow(get_horizontal_line())

    layout.addRow('Phone', QLineEdit())
    layout.addRow(get_horizontal_line())

    layout.addRow('Ok?', QCheckBox())

    mw = QWidget()
    mw.setLayout(layout)
    mw.show()

    app.exec()
