#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback

from PyQt5.QtWidgets import (
    QMessageBox,
    QMainWindow,
    QApplication,
    QUndoCommand,
    QUndoStack,
)
from PyQt5.QtGui import QPainter, QColor, QImage
from PyQt5.QtCore import Qt, QRectF


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


# SOURCE: https://github.com/gil9red/fake-painter/blob/8008f4b9a156e8363fce464310c20d229114af47/undocommand.py#L14
class UndoCommand(QUndoCommand):
    """
    Class which provides undo/redo actions
    """

    def __init__(self, canvas, parent=None):
        super().__init__(parent)

        self.mPrevImage = canvas.image.copy()
        self.mCurrImage = canvas.image.copy()

        self.canvas = canvas

    def undo(self):
        self.mCurrImage = self.canvas.image.copy()
        self.canvas.image = self.mPrevImage
        self.canvas.update()

    def redo(self):
        self.canvas.image = self.mCurrImage
        self.canvas.update()


class Widget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(600, 400)

        self.mUndoStack = QUndoStack(self)
        self.mUndoStack.setUndoLimit(100)

        self.mUndoStack.canUndoChanged.connect(self.can_undo_changed)
        self.mUndoStack.canRedoChanged.connect(self.can_redo_changed)

        self.actionUndo = self.menuBar().addAction("Undo")
        self.actionUndo.triggered.connect(self.mUndoStack.undo)

        self.actionRedo = self.menuBar().addAction("Redo")
        self.actionRedo.triggered.connect(self.mUndoStack.redo)

        self.can_undo_changed(self.mUndoStack.canUndo())
        self.can_redo_changed(self.mUndoStack.canRedo())

        self.image = QImage(self.size(), QImage.Format_ARGB32)
        self.image.fill(Qt.transparent)

        self.start_pos = None
        self.end_pos = None
        self.is_pressed = False

    def can_undo_changed(self, enabled):
        self.actionUndo.setEnabled(enabled)

    def can_redo_changed(self, enabled):
        self.actionRedo.setEnabled(enabled)

    def make_undo_command(self):
        self.mUndoStack.push(UndoCommand(self))

    def draw(self, canvas):
        painter = QPainter(canvas)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#AAFF0000"))

        painter.drawEllipse(QRectF(self.start_pos, self.end_pos))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.image.rect(), self.image)

        if self.is_pressed:
            self.draw(self)

    def mousePressEvent(self, event):
        self.is_pressed = True
        self.start_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.end_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        self.is_pressed = False
        self.end_pos = event.pos()

        self.make_undo_command()
        self.draw(self.image)

        self.update()


if __name__ == "__main__":
    app = QApplication([])

    w = Widget()
    w.show()

    app.exec()
