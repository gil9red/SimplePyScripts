#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


class MainWindow(Qt.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.sb_font_size = Qt.QSpinBox()
        self.sb_font_size.setRange(5, 40)
        self.sb_font_size.valueChanged.connect(self._on_font_size_changed)

        self.text_edit = Qt.QTextEdit("Test this!")

        layout = Qt.QVBoxLayout()
        layout.addWidget(self.sb_font_size)
        layout.addWidget(self.text_edit)

        central_widget = Qt.QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def _on_font_size_changed(self, value) -> None:
        text_char_format = Qt.QTextCharFormat()
        text_char_format.setFontPointSize(value)

        self.merge_format_on_word_or_selection(text_char_format)

    def merge_format_on_word_or_selection(self, text_char_format) -> None:
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            cursor.select(Qt.QTextCursor.WordUnderCursor)

        cursor.mergeCharFormat(text_char_format)


if __name__ == "__main__":
    app = Qt.QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
