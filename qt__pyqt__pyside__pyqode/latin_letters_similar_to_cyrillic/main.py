#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.stackoverflow.com/questions/839750/


import re

from PyQt5 import Qt
from PyQt5.uic import loadUi


class MainWindow(Qt.QWidget):
    def __init__(self):
        super().__init__()

        loadUi("main.ui", self)

        self.btn_solve.clicked.connect(self.solve)
        self.btn_clear.clicked.connect(self.textEdit_words.clear)

        self.textEdit_text.setPlainText("СВЕТА РОЕТ РОВ, ВОВКА СЕЕТ ОВЁС")

    def solve(self):
        # Исходный текст
        text = self.textEdit_text.toPlainText()

        # Буквы, совпадающие с английскими
        for word in re.findall(r"\b[АВСТРХОНКМУЕ]+\b", text):
            self.textEdit_words.append(word)


if __name__ == "__main__":
    app = Qt.QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
