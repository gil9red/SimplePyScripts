#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Идея взята из игры Assassin’s Creed


import random

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer


def get_random_text_progress(text: str) -> list[str]:
    items = []

    for i in range(1, len(text) + 1):
        chars = list(text)
        random.shuffle(chars)
        chars = chars[i:]

        new_text = text[:i] + "".join(chars)
        items.append(new_text)

    return items


class RandomTextProgress(QLabel):
    def __init__(self, text: str, msec: int = 300):
        super().__init__()

        self._text = text
        self._seq_text: list[str] = []

        self._timer = QTimer()
        self._timer.timeout.connect(self._on_tick)
        self._timer.start(msec)

        self._on_tick()

    def _on_tick(self):
        if not self._seq_text:
            self._seq_text = get_random_text_progress(self._text)

        self.setText(self._seq_text.pop(0))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        font = self.font()
        font.setPointSize(int(font.pointSize() * 1.5))
        self.setFont(font)

        layout = QVBoxLayout()
        layout.addWidget(RandomTextProgress(text="Download..."))
        layout.addWidget(RandomTextProgress(text="Download..."))
        layout.addWidget(RandomTextProgress(text="Download..."))
        layout.addWidget(QLabel())
        layout.addWidget(RandomTextProgress(text="Загрузка", msec=1000))

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
