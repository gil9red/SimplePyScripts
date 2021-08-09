#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QGridLayout
from PyQt5.QtCore import Qt, QEventLoop, QTimer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Main Form')
        self.resize(640, 480)

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        self.label = QLabel('<h1>Hello World.</h1>')
        self.layout = QGridLayout(self.centralwidget)
        self.layout.addWidget(self.label, 0, 0, alignment=Qt.AlignCenter)

        self._my_sleep(1500)

    def do_load(self):
        self._my_sleep(3000)

    def _my_sleep(self, ms: int):
        # NOTE: Для симуляции ожидания прогрузок
        loop = QEventLoop()
        QTimer.singleShot(ms, loop.quit)
        loop.exec()
