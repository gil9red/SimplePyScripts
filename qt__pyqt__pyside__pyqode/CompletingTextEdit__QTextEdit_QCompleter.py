#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback

from PyQt5.QtCore import QFile, QStringListModel, Qt
from PyQt5.QtGui import QCursor, QKeySequence, QTextCursor
from PyQt5.QtWidgets import (
    QApplication,
    QCompleter,
    QMainWindow,
    QTextEdit,
    QMessageBox,
)


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = "{}: {}:\n".format(ex_cls.__name__, ex)
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class CompletingTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.completerSequence = QKeySequence("Ctrl+Space")

        self._completer = QCompleter()
        self._completer.setWidget(self)
        self._completer.activated.connect(self.insertCompletion)

    def insertCompletion(self, completion):
        if self._completer.widget() is not self:
            return

        tc = self.textCursor()
        extra = len(completion) - len(self._completer.completionPrefix())
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)

    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)

        return tc.selectedText()

    def loadFromFile(self, fileName):
        f = QFile(fileName)
        if not f.open(QFile.ReadOnly):
            model = QStringListModel()
            self._completer.setModel(model)

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        words = []
        while not f.atEnd():
            line = f.readLine().trimmed()
            if line.length() != 0:
                try:
                    line = str(line, encoding="utf-8")
                except TypeError:
                    line = str(line)

                words.append(line)

        QApplication.restoreOverrideCursor()

        model = QStringListModel(words)
        self._completer.setModel(model)

    def loadFromList(self, words):
        model = QStringListModel(words)
        self._completer.setModel(model)

    def keyPressEvent(self, e):
        if self._completer.popup().isVisible():
            # The following keys are forwarded by the completer to the widget.
            if e.key() in (
                Qt.Key_Enter,
                Qt.Key_Return,
                Qt.Key_Escape,
                Qt.Key_Tab,
                Qt.Key_Backtab,
            ):
                e.ignore()
                # Let the completer do default behavior.
                return

        newSeq = QKeySequence(e.modifiers() | e.key())
        isShortcut = newSeq == self.completerSequence

        if not isShortcut:
            # Do not process the shortcut when we have a completer.
            super().keyPressEvent(e)
            return

        ctrlOrShift = e.modifiers() & (Qt.ControlModifier | Qt.ShiftModifier)
        if ctrlOrShift and not e.text():
            return

        eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="
        hasModifier = (e.modifiers() != Qt.NoModifier) and not ctrlOrShift
        completionPrefix = self.textUnderCursor()

        if not isShortcut and (
            hasModifier
            or not e.text()
            or len(completionPrefix) < 3
            or e.text()[-1] in eow
        ):
            self._completer.popup().hide()
            return

        if completionPrefix != self._completer.completionPrefix():
            self._completer.setCompletionPrefix(completionPrefix)
            self._completer.popup().setCurrentIndex(
                self._completer.completionModel().index(0, 0)
            )

        cr = self.cursorRect()
        cr.setWidth(
            self._completer.popup().sizeHintForColumn(0)
            + self._completer.popup().verticalScrollBar().sizeHint().width()
        )
        self._completer.complete(cr)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Completer")

        self.textEdit = CompletingTextEdit()

        self.textEdit.loadFromList(
            ["dog", "cat", "carry", "python", "собака", "foobar"]
        )
        # OR:
        # self.textEdit.loadFromFile('wordlist.txt')

        self.textEdit.setPlainText(
            "This TextEdit provides autocompletions for words that have "
            "more than 3 characters. You can trigger autocompletion "
            "using %s\n\n"
            % self.textEdit.completerSequence.toString(QKeySequence.NativeText)
        )

        self.setCentralWidget(self.textEdit)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.resize(500, 300)
    mw.show()

    sys.exit(app.exec_())
