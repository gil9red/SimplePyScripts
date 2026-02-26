#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from pathlib import Path

from PyQt5.Qt import QApplication, QWidget, QPixmap, QLabel, QTimer, QCursor, Qt


# SOURCE: http://www.pngall.com/target-png/download/12907
FILE_NAME = str(Path(__file__).resolve().parent / "target.png")


def move_window_to_cursor(widget: QWidget) -> None:
    width, height = widget.width(), widget.height()
    pos = QCursor.pos()
    pos.setX(int(pos.x() - width / 2))
    pos.setY(int(pos.y() - height / 2))

    widget.move(pos)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    lifetime_ms = 3000
    if len(sys.argv) == 2:
        lifetime_ms = int(sys.argv[1])

    pix = QPixmap(FILE_NAME)

    mw = QLabel()
    mw.setWindowFlag(Qt.WindowStaysOnTopHint)
    mw.setWindowFlag(Qt.FramelessWindowHint)
    mw.setPixmap(pix)
    mw.setMask(pix.mask())

    mw.show()

    move_window_to_cursor(mw)

    timer = QTimer()
    timer.timeout.connect(lambda: move_window_to_cursor(mw))
    timer.start(33)

    QTimer.singleShot(lifetime_ms, app.quit)

    app.exec()
