#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from threading import Thread

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QSizePolicy

import requests

from config import PORT


URL = 'http://127.0.0.1:%s/command/{}' % PORT


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        button_left = self._create_button('LEFT')
        button_right = self._create_button('RIGHT')
        button_top = self._create_button('TOP')
        button_bottom = self._create_button('BOTTOM')

        layout = QGridLayout(self)
        layout.setSpacing(0)
        layout.addWidget(button_left, 1, 0)
        layout.addWidget(button_right, 1, 2)
        layout.addWidget(button_top, 0, 1)
        layout.addWidget(button_bottom, 2, 1)

    def _create_button(self, data: str) -> QPushButton:
        button = QPushButton(data)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button.clicked.connect(lambda checked, data=data: self._on_click(data))

        return button

    def _send_command(self, data: str):
        rs = requests.post(URL.format(data))
        rs.raise_for_status()

    def _on_click(self, data: str):
        print(data)
        Thread(target=self._send_command, args=[data]).start()


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.resize(400, 400)
    mw.show()

    app.exec()
