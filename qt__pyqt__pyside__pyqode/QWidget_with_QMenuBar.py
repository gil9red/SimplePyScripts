#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


class MainWindow(Qt.QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        menu_bar = Qt.QMenuBar()
        menu_file = menu_bar.addMenu("File")
        action_exit = menu_file.addAction("Exit")
        action_exit.triggered.connect(self.close)

        layout = Qt.QVBoxLayout()
        layout.addWidget(Qt.QLabel("Test"))
        layout.addWidget(Qt.QPushButton("Click!"))

        layout.setMenuBar(menu_bar)

        self.setLayout(layout)


if __name__ == "__main__":
    app = Qt.QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
