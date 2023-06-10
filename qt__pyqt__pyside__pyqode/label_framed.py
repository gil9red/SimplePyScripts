#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


class Widget(Qt.QWidget):
    def __init__(self):
        super().__init__()

        layout = Qt.QVBoxLayout()
        layout.addWidget(self.create_label_framed("Hello"))
        layout.addWidget(self.create_label_framed("World"))
        layout.addWidget(self.create_label_framed("999"))

        self.setLayout(layout)

    @staticmethod
    def create_label_framed(text):
        label = Qt.QLabel(text)
        label.setFrameStyle(Qt.QFrame.Box)

        return label


if __name__ == "__main__":
    app = Qt.QApplication([])

    w = Widget()
    w.show()

    app.exec()
