#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.Qt import QWidget, QApplication, QPushButton, QVBoxLayout, QMessageBox


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        button = QPushButton("Close")
        button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(button)

        self.setLayout(layout)

    def closeEvent(self, event) -> None:
        reply = QMessageBox.question(
            self,
            "Quit",
            "Are you sure you want to quit?",
            QMessageBox.Yes,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
