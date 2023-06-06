#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QLineEdit, QApplication

from IP_Validator import get_ip_validator


if __name__ == "__main__":
    app = QApplication([])

    mw = QLineEdit()
    mw.setValidator(get_ip_validator())
    mw.setText("0.0.0.0")
    mw.show()

    app.exec()
