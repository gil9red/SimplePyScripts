#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


app = Qt.QApplication([])

te = Qt.QTextEdit()
te.setHtml(
    """
<b>Hello</b> <i>Qt!</i><br>
<font color="red"><b>Привет<b></font> <font size="20">мир!</font>
"""
)
te.show()

app.exec()
