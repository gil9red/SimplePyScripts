#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.button = QPushButton("Test")
        self.button.clicked.connect(self.on_clicked)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.button)

        self.setLayout(main_layout)

    def foo(self):
        print("foo")

    def bar(self):
        print("bar")

    def on_clicked(self):
        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.AltModifier:
            self.bar()
        else:
            self.foo()


if __name__ == "__main__":
    app = QApplication([])

    mw = Window()
    mw.show()

    app.exec()
