#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


class Widget(Qt.QWidget):
    def resizeEvent(self, event: Qt.QResizeEvent) -> None:
        width, height = event.size().width(), event.size().height()
        width = height = max(width, height)
        self.resize(width, height)


if __name__ == "__main__":
    app = Qt.QApplication([])

    w = Widget()
    w.show()

    app.exec()
