#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
import time

from typing import List

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QComboBox, QPushButton, QLabel
from PyQt5.QtCore import QThread, QTimer, QWaitCondition, QMutex


class Thread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._is_pause = False
        self.condition = QWaitCondition()
        self.mutex = QMutex()
        self.sum = 0

    def is_pause(self) -> bool:
        return self._is_pause

    def pause(self):
        self._is_pause = True

    def resume(self):
        self._is_pause = False
        self.condition.wakeAll()

    def run(self):
        while True:
            self.mutex.lock()
            if self._is_pause:
                self.condition.wait(self.mutex)
            self.sum += 1
            time.sleep(2)
            self.mutex.unlock()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.combobox_thread = QComboBox()
        self.combobox_thread.currentIndexChanged.connect(self._update_states)

        self.label_result = QLabel()

        self.button_add = QPushButton('Add')
        self.button_add.clicked.connect(self.add)

        self.button_pause = QPushButton('Pause')
        self.button_pause.clicked.connect(self.pause)

        self.button_pause_all = QPushButton('Pause all')
        self.button_pause_all.clicked.connect(self.pause_all)

        self.button_resume = QPushButton('Resume')
        self.button_resume.clicked.connect(self.resume)

        self.button_resume_all = QPushButton('Resume all')
        self.button_resume_all.clicked.connect(self.resume_all)

        layout = QGridLayout(self)
        layout.addWidget(self.combobox_thread, 0, 0)
        layout.addWidget(self.button_add, 0, 1, 1, 2)
        layout.addWidget(self.label_result, 1, 0)
        layout.addWidget(self.button_pause, 1, 1)
        layout.addWidget(self.button_pause_all, 1, 2)
        layout.addWidget(self.button_resume, 2, 1)
        layout.addWidget(self.button_resume_all, 2, 2)
        layout.setRowStretch(layout.rowCount(), 1)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(1000)

        self._update_states()

    def _update_states(self):
        self.setWindowTitle(f'Threads: {self.combobox_thread.count()}')

        idx = self.combobox_thread.currentIndex()
        ok = idx != -1

        self.button_pause.setEnabled(ok and not self.get_thread(idx).is_pause())
        self.button_resume.setEnabled(ok and self.get_thread(idx).is_pause())

        if ok:
            title = self.combobox_thread.itemText(idx)
            self.button_pause.setText(f'Pause - {title!r}')
            self.button_resume.setText(f'Resume - {title!r}')

    def get_thread(self, idx: int) -> Thread:
        return self.combobox_thread.itemData(idx)

    def get_all_thread(self) -> List[Thread]:
        return [self.get_thread(i) for i in range(self.combobox_thread.count())]

    def update_info(self):
        total = sum(thread.sum for thread in self.get_all_thread())
        self.label_result.setText(f"SUM: <b>{total}</b>")

    def add(self):
        thread = Thread(self)
        thread.start()

        self.combobox_thread.addItem(f'Thread #{self.combobox_thread.count() + 1}', thread)
        self._update_states()

    def pause(self):
        thread = self.combobox_thread.currentData()
        if thread:
            thread.pause()

        self._update_states()

    def pause_all(self):
        for thread in self.get_all_thread():
            thread.pause()

        self._update_states()

    def resume(self):
        thread = self.combobox_thread.currentData()
        if thread:
            thread.resume()

        self._update_states()

    def resume_all(self):
        for thread in self.get_all_thread():
            thread.resume()

        self._update_states()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.resize(320, 240)
    mw.show()

    sys.exit(app.exec_())
