#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class ImageLabel(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setScene(QGraphicsScene())
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def setImage(self, filename: str):
        self.setPixmap(QPixmap(filename))

    def setPixmap(self, pixmap: QPixmap):
        item = QGraphicsPixmapItem(pixmap)
        item.setTransformationMode(Qt.SmoothTransformation)
        self.scene().addItem(item)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        rect = self.scene().itemsBoundingRect()
        self.fitInView(rect, Qt.KeepAspectRatio)


if __name__ == '__main__':
    app = QApplication([])

    screenshot = app.primaryScreen().grabWindow(QApplication.desktop().winId())

    w = ImageLabel()
    w.setPixmap(screenshot)
    w.show()

    app.exec()
