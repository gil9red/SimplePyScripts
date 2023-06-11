#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# http://doc.qt.io/qt-5/animation-overview.html


from PyQt5 import Qt


class MainWindow(Qt.QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = Qt.QLabel("Animated label", parent=self)
        self.label.move(0, 50)

        self.button = Qt.QPushButton("Start!", parent=self, clicked=self._on_click)

        self.animation = Qt.QPropertyAnimation(self.label, b"geometry")
        self.animation.setDuration(10000)
        self.animation.setStartValue(Qt.QRect(0, 0, 100, 30))
        self.animation.setEndValue(Qt.QRect(250, 250, 100, 30))

    def _on_click(self):
        self.animation.start()


if __name__ == "__main__":
    app = Qt.QApplication([])

    mw = MainWindow()
    mw.resize(500, 500)
    mw.show()

    app.exec()
