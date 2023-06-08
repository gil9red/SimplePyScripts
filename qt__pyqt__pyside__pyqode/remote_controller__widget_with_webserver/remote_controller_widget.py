#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path
from threading import Thread

import requests

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QGridLayout,
    QPushButton,
    QSizePolicy,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, Qt

from config import PORT


URL = "http://127.0.0.1:%s/command/{}" % PORT


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(Path(__file__).name)

        button_left = self._create_button("LEFT")
        button_right = self._create_button("RIGHT")
        button_top = self._create_button("UP")
        button_bottom = self._create_button("DOWN")

        button_hide = self._create_button("HIDE", False)
        button_show = self._create_button("SHOW", False)
        button_move_to_cursor = self._create_button("MOVE_TO_CURSOR", False)

        self.label_image = QLabel()
        self.label_image.setFrameStyle(QLabel.Box)
        self.label_image.setFixedSize(400, 400)

        layout = QGridLayout(self)
        layout.setSpacing(5)
        layout.addWidget(button_hide, 0, 0, Qt.AlignTop | Qt.AlignLeft)
        layout.addWidget(button_show, 0, 2, Qt.AlignTop | Qt.AlignRight)
        layout.addWidget(button_left, 1, 0)
        layout.addWidget(button_right, 1, 2)
        layout.addWidget(button_top, 0, 1)
        layout.addWidget(button_bottom, 2, 1)
        layout.addWidget(self.label_image, 3, 0, 3, 3)
        layout.addWidget(button_move_to_cursor, 2, 0, Qt.AlignBottom | Qt.AlignLeft)

        self.timer = QTimer()
        self.timer.timeout.connect(self._on_tick)
        self.timer.start(100)

    def _create_button(self, data: str, expanding=True) -> QPushButton:
        button = QPushButton(data)

        if expanding:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        button.clicked.connect(lambda checked, data=data: self._on_click(data))

        return button

    def _send_command(self, data: str):
        try:
            rs = requests.post(URL.format(data))
            rs.raise_for_status()

            if data == "SCREENSHOT":
                pixmap = QPixmap()
                pixmap.loadFromData(rs.content)

                pixmap = pixmap.scaled(self.label_image.size())
                self.label_image.setPixmap(pixmap)

        except:
            pass

    def _on_click(self, data: str):
        Thread(target=self._send_command, args=[data]).start()

    def _on_tick(self):
        Thread(target=self._send_command, args=["SCREENSHOT"]).start()


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.resize(400, 400 + 400)
    mw.show()

    app.exec()
