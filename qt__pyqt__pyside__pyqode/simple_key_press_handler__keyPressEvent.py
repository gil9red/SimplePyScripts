#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt


class MainWindow(QLabel):
    def keyPressEvent(self, event: QKeyEvent) -> None:
        super().keyPressEvent(event)

        text = f"{event.key()} : {event.text()!r}"
        print(text)

        self.setText(text)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.setAlignment(Qt.AlignCenter)
    mw.resize(200, 200)
    mw.show()

    app.exec()
