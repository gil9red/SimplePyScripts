#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


if __name__ == "__main__":
    app = Qt.QApplication([])

    # NOTE: для отладки
    # label = Qt.QLabel()

    def get_color():
        rect = button.rect()
        indent = 5

        pixmap = app.primaryScreen().grabWindow(
            button.winId(), rect.x(), rect.y() - indent, indent, indent
        )
        # label.setPixmap(pixmap)
        # label.setScaledContents(True)
        # label.resize(400, 400)
        # label.show()

        color = pixmap.toImage().pixelColor(0, 0)
        button.setStyleSheet("background-color: " + color.name())

    button = Qt.QPushButton("Get")
    button.clicked.connect(get_color)
    button.resize(100, 100)
    button.show()

    app.exec()
