#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from multiprocessing import current_process

# pip install psutil
import psutil

from PyQt5.Qt import QApplication, QWidget, QLabel, QTimer, QVBoxLayout


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._label_info = QLabel()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self._label_info)
        self.setLayout(main_layout)

        pid = current_process().pid
        self._process = psutil.Process(pid)

        self._timer = QTimer()
        self._timer.timeout.connect(self.update_memory_info)
        self._timer.start(500)

        self.update_memory_info()

    def update_memory_info(self):
        memory_bytes = self._process.memory_info().rss

        self._label_info.setText(
            f"Current memory: {memory_bytes} bytes\n"
            f"Current memory: {memory_bytes // 1024} KB\n"
            f"Current memory: {memory_bytes // 1024 // 1024} MB"
        )


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWidget()
    mw.show()

    app.exec()
