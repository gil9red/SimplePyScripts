#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Заполнение списка из функции без фриза окна. Вариант с QApplication.processEvents.

"""


import traceback
import sys

from PyQt5.QtWidgets import QWidget, QListWidget, QApplication, QVBoxLayout


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))

    print('Error: ', text)


sys.excepthook = log_uncaught_exceptions


def generator_large_list():
    for i in range(1000000):
        QApplication.processEvents()
        yield i


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.lw = QListWidget()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.lw)

        self.setLayout(layout)

    def fill(self):
        for i in generator_large_list():
            self.lw.addItem(str(i))
            self.lw.scrollToBottom()

    def closeEvent(self, event):
        # После закрытия окна приложение не завершится пока список работает
        sys.exit()


if __name__ == '__main__':
    app = QApplication([])

    w = Widget()
    w.show()
    w.fill()

    app.exec_()
