#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.Qt import Qt


class EgoDialog(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        # Задний фон не будет нарисован, это нужно чтобы через paintEvent его рисовать
        self.setAttribute(Qt.WA_TranslucentBackground)

    @staticmethod
    def exec(title: str, text: str) -> bool:
        mw = EgoDialog()
        mw.showFullScreen()

        ok = QMessageBox.question(mw, title, text)
        mw.close()

        return ok == QMessageBox.Yes

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setBrush(QColor(0, 0, 0, 127))
        painter.drawRect(self.rect())


if __name__ == "__main__":
    app = QApplication([])

    ok = EgoDialog.exec("Question", "Question?")
    if ok:
        print("User select Ok")
    else:
        print("User select No")

    # app.exec()
