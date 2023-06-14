#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from multiprocessing import current_process

# pip install psutil
import psutil

from PyQt5.Qt import (
    QApplication,
    QWidget,
    QLabel,
    QTimer,
    QVBoxLayout,
    QPushButton,
    QSpinBox,
    QHBoxLayout,
)


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._label_info = QLabel()

        self._button_append = QPushButton("Add")
        self._button_append.clicked.connect(self._on_append_clicked)

        self._spin_box_numbers = QSpinBox()
        self._spin_box_numbers.setRange(1, 1_000_000)
        self._spin_box_numbers.setValue(1_000_000)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self._button_append)
        h_layout.addWidget(self._spin_box_numbers)
        h_layout.addWidget(QLabel("objects"))

        main_layout = QVBoxLayout()
        main_layout.addWidget(self._label_info)
        main_layout.addLayout(h_layout)
        self.setLayout(main_layout)

        self._items = []

        pid = current_process().pid
        self._process = psutil.Process(pid)

        self._timer = QTimer()
        self._timer.timeout.connect(self.update_memory_info)
        self._timer.start(500)

        self.update_memory_info()

    def _on_append_clicked(self):
        row = [0 for _ in range(self._spin_box_numbers.value())]
        self._items.append(row)

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
