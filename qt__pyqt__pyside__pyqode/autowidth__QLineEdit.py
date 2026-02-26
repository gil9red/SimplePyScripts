#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


class Widget(Qt.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.line_edit = Qt.QLineEdit()
        self.line_edit.textChanged.connect(self.on_text_changed)

        layout = Qt.QVBoxLayout()
        layout.addWidget(self.line_edit)

        self.setLayout(layout)

    def on_text_changed(self, text) -> None:
        # Рассчитываем ширину текст по шрифту
        width = self.line_edit.fontMetrics().width(text)
        self.line_edit.setMinimumWidth(width)


if __name__ == "__main__":
    app = Qt.QApplication([])

    mw = Widget()
    mw.show()

    app.exec()
