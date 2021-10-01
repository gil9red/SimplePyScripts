#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import QApplication, QWidget, QToolButton, QSizePolicy
from PyQt5.QtGui import QResizeEvent


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            MainWindow {
                background-color: black;
            }
            
            QToolButton {
                color : white;
                background-color: black;
                border: 1px solid darkgray;
            }
        """)

        self.button_close = QToolButton(self)
        self.button_close.setText('ЗАКРЫТЬ')
        self.button_close.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.button_close.clicked.connect(self.close)

    def resizeEvent(self, event: QResizeEvent):
        size = event.size()
        size = min(size.width(), size.height()) // 4
        self.button_close.resize(size, size)


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.resize(600, 600)
    # mw.show()
    mw.showFullScreen()

    app.exec()
