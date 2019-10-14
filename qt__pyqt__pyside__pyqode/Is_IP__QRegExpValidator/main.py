#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import QLineEdit, QApplication
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression

from is_ip import IP_REGEXP


if __name__ == '__main__':
    app = QApplication([])

    mw = QLineEdit()
    mw.setValidator(QRegularExpressionValidator(QRegularExpression(IP_REGEXP)))
    mw.setText("0.0.0.0")
    mw.show()

    app.exec()
