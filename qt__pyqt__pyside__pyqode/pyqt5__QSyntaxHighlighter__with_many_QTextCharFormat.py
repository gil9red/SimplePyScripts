#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.Qt import *


class MyHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)

        self.regexp_by_format = dict()

        char_format = QTextCharFormat()
        char_format.setFontWeight(QFont.Bold)
        char_format.setForeground(Qt.darkMagenta)
        self.regexp_by_format[r"\bsin\b"] = char_format

        char_format = QTextCharFormat()
        char_format.setFontWeight(QFont.Bold)
        char_format.setFontItalic(True)
        char_format.setForeground(Qt.darkCyan)
        self.regexp_by_format[r"\bcos\b"] = char_format

    def highlightBlock(self, text):
        for regexp, char_format in self.regexp_by_format.items():
            expression = QRegularExpression(regexp)
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(
                    match.capturedStart(), match.capturedLength(), char_format
                )


if __name__ == "__main__":
    app = QApplication([])

    mw = QTextEdit()
    mw.setText("x = sin(1)\nb = cos(sin(PI));")

    highlighter = MyHighlighter(mw.document())

    mw.show()

    app.exec()
