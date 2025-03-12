#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtCore import Qt, QRegularExpression
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont
from PyQt5.QtWidgets import QApplication, QPlainTextEdit, QTextEdit


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

    text_edit = QTextEdit()
    text_edit.setWindowTitle("QTextEdit")
    text_edit.setText("x = sin(1)\nb = cos(sin(PI));")
    highlighter_text_edit = MyHighlighter(text_edit.document())
    text_edit.show()

    plain_text_edit = QPlainTextEdit()
    plain_text_edit.setWindowTitle("QPlainTextEdit")
    plain_text_edit.setPlainText(text_edit.toPlainText())
    highlighter_plain_text_edit = MyHighlighter(plain_text_edit.document())
    plain_text_edit.show()

    pos = text_edit.pos()
    pos.setX(pos.x() + text_edit.width() + 5)
    plain_text_edit.move(pos)

    app.exec()
