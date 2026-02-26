#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QWidget,
    QLabel,
    QStackedWidget,
    QListWidget,
)


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(QLabel("1234"))
        self.stacked_widget.addWidget(QLabel("ABCD"))
        self.stacked_widget.addWidget(QLabel("FOO_BAR"))

        self.control_list = QListWidget()
        self.control_list.addItems(["1234", "ABCD", "FOO_BAR"])
        self.control_list.setFixedWidth(80)
        self.control_list.clicked.connect(
            lambda index: self.stacked_widget.setCurrentIndex(index.row())
        )

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.control_list)
        main_layout.addWidget(self.stacked_widget)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
