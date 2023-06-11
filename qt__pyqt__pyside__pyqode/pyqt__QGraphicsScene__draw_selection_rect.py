#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import (
    QGraphicsScene,
    QGraphicsView,
    QMainWindow,
    QApplication,
    QGraphicsRectItem,
)
from PyQt5.QtCore import QRectF, QPointF, Qt
from PyQt5.QtGui import QColor, QPainter


class GraphicsScene(QGraphicsScene):
    def __init__(self):
        super().__init__()

        self._pos = QPointF()
        self._current_item = None

        # Полупрозрачный цвет
        self._item_color = QColor(0, 0, 255, 128)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        self._pos = event.scenePos()

        self._current_item = QGraphicsRectItem()
        self._current_item.setBrush(self._item_color)

        self.addItem(self._current_item)
        self._current_item.setRect(QRectF(self._pos, self._pos))

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        if self._current_item:
            rect = QRectF(self._pos, event.scenePos()).normalized()
            self._current_item.setRect(rect)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        # Убираем после отпускания кнопки мыши
        self.removeItem(self._current_item)
        self._current_item = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        scene_rect = QRectF(0, 0, 500, 500)

        self.scene = GraphicsScene()

        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setSceneRect(scene_rect)
        self.view.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.scene.addRect(0, 0, 200, 100)
        self.scene.addEllipse(100, 50, 200, 200)
        self.scene.addText("Hello World!").setPos(300, 300)

        self.setCentralWidget(self.view)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.resize(600, 600)
    mw.show()

    app.exec()
