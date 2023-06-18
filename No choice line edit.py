#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт показывает пример ограничение ввода только тем текстом, что был указан.

"""


from PyQt5.QtWidgets import *


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("No choice")

        self.line_edit_no_choice = QLineEdit()
        self.line_edit_no_choice.textEdited.connect(self.on_text_edited_no_choice)

        self.line_edit_source = QLineEdit("Я придурок")
        self.line_edit_source.textEdited.connect(self.line_edit_no_choice.clear)

        layout = QFormLayout()
        layout.addRow("Скажи:", self.line_edit_source)
        layout.addWidget(self.line_edit_no_choice)

        self.setLayout(layout)

        self.line_edit_no_choice.setFocus()

    def on_text_edited_no_choice(self, text):
        text = self.line_edit_source.text()[: len(text)]
        self.line_edit_no_choice.setText(text)


if __name__ == "__main__":
    app = QApplication([])

    w = Widget()
    w.show()

    app.exec()
