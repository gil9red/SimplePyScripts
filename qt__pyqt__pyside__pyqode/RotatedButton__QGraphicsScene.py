#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "ipetrash"


import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsLinearLayout,
    QGraphicsWidget,
    QHBoxLayout,
)
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 200, 200)

        self.view = QGraphicsView()
        self.view.setRenderHint(QPainter.HighQualityAntialiasing)
        self.view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.view.setScene(self.scene)

        scene_layout = QGraphicsLinearLayout(Qt.Horizontal)

        form = QGraphicsWidget()
        form.setLayout(scene_layout)

        self.scene.addItem(form)

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.view)
        self.setLayout(self.main_layout)

        self.rb0 = QPushButton("Hello")
        proxy_rb0 = self.scene.addWidget(self.rb0)
        scene_layout.addItem(proxy_rb0)

        self.rb1 = QPushButton("Hello")
        proxy_rb1 = self.scene.addWidget(self.rb1)
        proxy_rb1.setRotation(90)
        scene_layout.addItem(proxy_rb1)

        self.rb2 = QPushButton("Hello")
        proxy_rb2 = self.scene.addWidget(self.rb2)
        proxy_rb2.setRotation(180)
        scene_layout.addItem(proxy_rb2)

        self.rb3 = QPushButton("Hello")
        proxy_rb3 = self.scene.addWidget(self.rb3)
        proxy_rb3.setRotation(-166)
        scene_layout.addItem(proxy_rb3)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = Window()
    w.setMinimumSize(0, 200)
    w.show()

    sys.exit(app.exec_())
