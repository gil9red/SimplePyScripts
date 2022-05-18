#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QLabel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        label_result = QLabel()

        button_left = QPushButton('Left')
        button_left.setShortcut("Ctrl+Alt+Left")
        button_left.clicked.connect(lambda: label_result.setText("left"))

        button_right = QPushButton('Right')
        button_right.setShortcut("Ctrl+Alt+Right")
        button_right.clicked.connect(lambda: label_result.setText("right"))

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(button_left)
        main_layout.addWidget(label_result)
        main_layout.addWidget(button_right)


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
