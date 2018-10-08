#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.Qt import *


app = QApplication([])

list_widget = QListWidget()
list_widget.addItems(map(str, range(1, 100 + 1)))
list_widget.setFlow(QListView.LeftToRight)
list_widget.setWrapping(True)
list_widget.setUniformItemSizes(True)
list_widget.show()

app.exec()
