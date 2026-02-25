#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Фрактальное дерево / Fractal tree

"""

import math
import io

from PIL import Image, ImageDraw

try:
    from PyQt5.QtWidgets import (
        QApplication,
        QWidget,
        QLabel,
        QPushButton,
        QVBoxLayout,
        QSizePolicy,
    )
    from PyQt5.QtGui import QImage, QPixmap, QPainter
    from PyQt5.QtCore import Qt

except ImportError:
    try:
        from PyQt4.QtGui import (
            QImage,
            QPainter,
            QApplication,
            QWidget,
            QLabel,
            QPushButton,
            QVBoxLayout,
            QSizePolicy,
            QPixmap,
        )
        from PyQt4.QtCore import Qt

    except ImportError:
        from PySide.QtGui import (
            QImage,
            QPainter,
            QApplication,
            QWidget,
            QLabel,
            QPushButton,
            QVBoxLayout,
            QSizePolicy,
            QPixmap,
        )
        from PySide.QtCore import Qt

from Fractal_tree__PIL import draw_fractal_tree


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Fractal tree")

        self.img_label = QLabel()
        self.img_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.generate_tree_button = QPushButton("Generate Tree")
        self.generate_tree_button.clicked.connect(self.generate_tree)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.generate_tree_button)
        main_layout.addWidget(self.img_label)

        self.setLayout(main_layout)

    def generate_tree(self) -> None:
        img = Image.new("RGB", (700, 600), "white")

        draw_fractal_tree(ImageDraw.Draw(img), 350, 580, 3 * math.pi / 2, 200)

        img_bytes_io = io.BytesIO()
        img.save(img_bytes_io, format="PNG")
        img_bytes = img_bytes_io.getvalue()

        img = QPixmap()
        img.loadFromData(img_bytes)

        self.img_label.setPixmap(img)


if __name__ == "__main__":
    app = QApplication([])

    w = Widget()
    w.resize(700, 600)
    w.show()
    w.generate_tree()

    app.exec()
