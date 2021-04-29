#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Заполнение списка из функции без фриза окна. Вариант с QThread.

"""


import sys
import time
import traceback

from PyQt5.QtWidgets import QWidget, QListWidget, QApplication, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))

    print('Error: ', text)


sys.excepthook = log_uncaught_exceptions


class MyThread(QThread):
    about_new_value = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.executed = False

    def run(self):
        print('start thread')

        try:
            for i in range(1000000):
                if not self.executed:
                    break

                self.about_new_value.emit(i)
                print(i)

                # Задержка в 5 миллисекунд
                time.sleep(0.005)

        finally:
            print('finish thread')

    def start(self, priority=QThread.InheritPriority):
        self.executed = True

        return super().start(priority)

    def exit(self, returnCode=0):
        self.executed = False

        return super().exit(returnCode)


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.lw = QListWidget()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.lw)

        self.setLayout(layout)

        self.thread = MyThread()
        self.thread.about_new_value.connect(lambda x: self.append_item(str(x)))

    def append_item(self, item):
        self.lw.addItem(item)
        self.lw.scrollToBottom()

    def fill(self):
        self.thread.start()

    def closeEvent(self, event):
        # После закрытия окна приложение не завершится пока список работает
        sys.exit()


if __name__ == '__main__':
    app = QApplication([])

    w = Widget()
    w.show()
    w.fill()

    app.exec_()
