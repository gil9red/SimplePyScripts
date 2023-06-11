#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import *


app = QApplication([])

# По стандарту ISO 9564-1 ПИН может содержать от 4 до 12 десятичных цифр.
label_pin = QLabel()
line_edit_pin = QLineEdit()
line_edit_pin.setInputMask("999900000000")
line_edit_pin.textEdited.connect(
    lambda text: label_pin.setText('PIN: "{}"'.format(text))
)

# Payment card numbers can be up to 19 digits
label_pan = QLabel()
line_edit_pan = QLineEdit()
line_edit_pan.setInputMask("9999 9999 9999 0000 000")
line_edit_pan.textEdited.connect(
    lambda text: label_pan.setText('PAN: "{}"'.format(text))
)

layout = QFormLayout()
layout.addRow("PIN:", line_edit_pin)
layout.addRow(label_pin)
layout.addRow(QLabel())
layout.addRow("PAN:", line_edit_pan)
layout.addRow(label_pan)

w = QWidget()
w.setLayout(layout)
w.show()

app.exec()
