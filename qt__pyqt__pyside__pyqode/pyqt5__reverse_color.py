#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.Qt import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QColorDialog,
    QFont,
)


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.button = QPushButton("Color")
        self.button.setFont(QFont("Times", 16))
        self.button.clicked.connect(self.choose_color)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.button)
        self.setLayout(main_layout)

    def choose_color(self):
        dialog = QColorDialog()
        if not dialog.exec():
            return

        red, green, blue, _ = dialog.currentColor().getRgb()

        # Reverse color
        red, green, blue = 255 - red, 255 - green, 255 - blue

        self.button.setStyleSheet(
            f"background: {dialog.currentColor().name()}; color: rgb({red}, {green}, {blue});"
        )


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
