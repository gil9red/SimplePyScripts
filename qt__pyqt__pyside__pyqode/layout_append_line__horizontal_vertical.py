#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import QFrame


def get_horizontal_line() -> QFrame:
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setFrameShadow(QFrame.Sunken)
    line.setLineWidth(1)
    return line


def get_vertical_line() -> QFrame:
    line = QFrame()
    line.setFrameShape(QFrame.VLine)
    line.setFrameShadow(QFrame.Sunken)
    line.setLineWidth(1)
    return line


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QFormLayout, QHBoxLayout, QLineEdit, QCheckBox, QWidget, QLabel
    from PyQt5.QtCore import Qt

    app = QApplication([])

    layout = QFormLayout()
    layout.addRow('First', QLineEdit())
    layout.addRow('Last', QLineEdit())
    layout.addRow(get_horizontal_line())

    layout.addRow('Phone', QLineEdit())
    layout.addRow(get_horizontal_line())

    h_layout = QHBoxLayout()
    label = QLabel("1")
    label.setAlignment(Qt.AlignCenter)
    h_layout.addWidget(label)
    h_layout.addWidget(get_vertical_line())

    label = QLabel("2")
    label.setAlignment(Qt.AlignCenter)
    h_layout.addWidget(label)
    h_layout.addWidget(get_vertical_line())

    label = QLabel("3")
    label.setAlignment(Qt.AlignCenter)
    h_layout.addWidget(label)

    layout.addItem(h_layout)

    layout.addRow('Ok?', QCheckBox())

    mw = QWidget()
    mw.setLayout(layout)
    mw.show()

    app.exec()
