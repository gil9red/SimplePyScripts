#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.Qt import *


class MyHighlighter(QSyntaxHighlighter):
    def highlightBlock(self, text):
        char_format = QTextCharFormat()
        char_format.setFontWeight(QFont.Bold)
        char_format.setForeground(Qt.darkMagenta)

        expression = QRegularExpression(r"\b(cos|sin)\b")
        it = expression.globalMatch(text)
        while it.hasNext():
            match = it.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), char_format)


if __name__ == "__main__":
    app = QApplication([])

    mw = QTextEdit()
    mw.setText("x = sin(1)\nb = cos(sin(PI));")

    highlighter = MyHighlighter(mw.document())

    mw.show()

    app.exec()
