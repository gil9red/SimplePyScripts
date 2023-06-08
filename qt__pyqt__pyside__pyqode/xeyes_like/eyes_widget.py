#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QCursor, QResizeEvent, QCloseEvent
from PyQt5.QtCore import QTimer, QPoint, Qt

from eye_widget import UEyeWidget


# TODO:
d_indentTop = 20
d_indentLeft = 4
d_indentRight = 4
d_indentBottom = 4
d_indentBetweenEyes = 1


# TODO: rename
class UEyesWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.eyes: list[UEyeWidget] = [UEyeWidget(self) for _ in range(2)]

        self.timerCursorPos = QTimer(self)
        self.timerCursorPos.timeout.connect(self.refreshLookThere)
        self.timerCursorPos.start(30)

        self.setTopOfAllWindows(True)

    def refreshLookThere(self):
        self.update()

        position: QPoint = QCursor.pos()
        for eye in self.eyes:
            eye.lookThere(position)

    def setTopOfAllWindows(self, top: bool):
        oldPos: QPoint = self.pos()

        if top:
            flags = Qt.Tool | Qt.WindowStaysOnTopHint
        else:
            flags = Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnBottomHint

        self.setWindowFlags(flags)

        self.showNormal()
        self.move(oldPos)

    def updateMinimumSize(self):
        if not self.eyes:
            return

        widthEye: int = self.eyes[0].width()
        heightEye: int = self.eyes[0].height()

        sumIndent: int = (len(self.eyes) - 1) * d_indentBetweenEyes

        sumWidthEyes: int = len(self.eyes) * widthEye

        minWidth = sumWidthEyes + d_indentLeft + d_indentRight + sumIndent
        minHeight = heightEye + d_indentTop + d_indentBottom

        self.setMinimumSize(
            minWidth + d_indentLeft + d_indentRight,
            minHeight + d_indentTop + d_indentBottom,
        )

    def updateSize(self):
        self.updateMinimumSize()
        QApplication.instance().postEvent(self, QResizeEvent(self.size(), self.size()))

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)

        if not self.eyes:
            return

        x: int = d_indentLeft
        y: int = d_indentRight

        w = (
            event.size().width()
            - (d_indentLeft + d_indentRight)
            - (len(self.eyes) - 1) * d_indentBetweenEyes
        ) / len(self.eyes)
        h = event.size().height() - (d_indentTop + d_indentBottom)

        diameter: int = int(min(w, h))

        for eye in self.eyes:
            eye.move(x, y)
            eye.setFixedSize(diameter, diameter)
            # eye.resize(diameter, diameter)  # TODO: В версии c++ этот код работал

            x = eye.x() + eye.width() + d_indentBetweenEyes

    def closeEvent(self, _: QCloseEvent):
        QApplication.instance().quit()
