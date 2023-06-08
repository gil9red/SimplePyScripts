#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import glob
import json

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QDockWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QPlainTextEdit,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._current_index_image = 0
        self._images = glob.glob("images/*.png")
        self._data = dict()

        self.label_image = QLabel()
        self.label_image.setFixedSize(400, 400)
        self.label_image.setScaledContents(True)

        self.line_edit_key = QLineEdit()
        self.line_edit_key.setPlaceholderText("Введите ключ картинки...")

        self.button_add_file_name = QPushButton("Добавить картинку")
        self.button_add_file_name.clicked.connect(self._on_add_file_name)

        self.button_prev = QPushButton("Предыдущая картинка")
        self.button_prev.clicked.connect(self.load_prev_image)

        self.button_next = QPushButton("Следующая картинка")
        self.button_next.clicked.connect(self.load_next_image)

        layout_control = QHBoxLayout()
        layout_control.addWidget(QLabel("Ключ:"))
        layout_control.addWidget(self.line_edit_key)
        layout_control.addWidget(self.button_add_file_name)

        layout_control_2 = QHBoxLayout()
        layout_control_2.addWidget(self.button_prev)
        layout_control_2.addWidget(self.button_next)

        self.pl_text_json = QPlainTextEdit()

        self._dock_widget = QDockWidget("JSON")
        self._dock_widget.setWidget(self.pl_text_json)

        self.addDockWidget(Qt.RightDockWidgetArea, self._dock_widget)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label_image)
        main_layout.addLayout(layout_control)
        main_layout.addLayout(layout_control_2)
        main_layout.addStretch()

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

        self.load_current_image()

    def get_current_image_file_name(self):
        return self._images[self._current_index_image]

    def load_prev_image(self):
        self._current_index_image -= 1
        if self._current_index_image < 0:
            self._current_index_image = 0

        self.load_current_image()

    def load_next_image(self):
        self._current_index_image += 1
        if self._current_index_image >= len(self._images):
            self._current_index_image = len(self._images) - 1

        self.load_current_image()

    def load_current_image(self):
        self.update_states()

        file_name = self.get_current_image_file_name()

        pixmap = QPixmap()
        pixmap.load(file_name)
        self.label_image.setPixmap(pixmap)

    def _on_add_file_name(self):
        key = self.line_edit_key.text()
        file_name = self.get_current_image_file_name()

        if key not in self._data:
            self._data[key] = []

        if file_name not in self._data[key]:
            self._data[key].append(file_name)

        self.pl_text_json.setPlainText(
            json.dumps(self._data, indent=4, ensure_ascii=False)
        )

    def update_states(self):
        file_name = self.get_current_image_file_name()
        self.setWindowTitle(
            f"{self._current_index_image + 1} / {len(self._images)} : {file_name}"
        )


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
