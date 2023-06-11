#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.Qt import *


class WrapListWidget(QListWidget):
    def __init__(self):
        super().__init__()

        self.setFlow(QListView.LeftToRight)
        self.setWrapping(True)
        self.setUniformItemSizes(True)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.setWrapping(self.isWrapping())


if __name__ == "__main__":
    app = QApplication([])

    list_widget = WrapListWidget()
    list_widget.addItems(map(str, range(1, 100 + 1)))
    list_widget.show()

    app.exec()
