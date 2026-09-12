#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QVBoxLayout, QMessageBox
from PyQt6.QtGui import QCloseEvent


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        button = QPushButton("Close")
        button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(button)

        self.setLayout(layout)

    def closeEvent(self, event: QCloseEvent | None) -> None:
        if not event:
            return

        reply = QMessageBox.question(
            self,
            "Quit",
            "Are you sure you want to quit?",
            QMessageBox.StandardButton.Yes,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    sys.exit(app.exec())
