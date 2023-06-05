#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
    QStackedWidget,
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(QLabel("1234"))
        self.stacked_widget.addWidget(QLabel("ABCD"))
        self.stacked_widget.addWidget(QLabel("FOO_BAR"))

        self.button_123 = QPushButton("1234")
        self.button_123.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        self.button_ABCD = QPushButton("ABCD")
        self.button_ABCD.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        self.button_FOO_BAR = QPushButton("FOO_BAR")
        self.button_FOO_BAR.clicked.connect(
            lambda: self.stacked_widget.setCurrentIndex(2)
        )

        layout_buttons = QVBoxLayout()
        layout_buttons.addWidget(self.button_123)
        layout_buttons.addWidget(self.button_ABCD)
        layout_buttons.addWidget(self.button_FOO_BAR)

        main_layout = QHBoxLayout(self)
        main_layout.addLayout(layout_buttons)
        main_layout.addWidget(self.stacked_widget)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
