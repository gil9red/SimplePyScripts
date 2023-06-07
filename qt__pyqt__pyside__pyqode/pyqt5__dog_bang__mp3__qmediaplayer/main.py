#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "ipetrash"


import traceback
import sys

from PyQt5 import Qt


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = "{}: {}:\n".format(ex_cls.__name__, ex)
    text += "".join(traceback.format_tb(tb))

    print(text)
    Qt.QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class Widget(Qt.QLabel):
    dog_sound_1 = "dog_sound_1.mp3"
    dog_sound_2 = "dog_sound_2.mp3"

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dog Bang!")

        self.setPixmap(Qt.QPixmap("dog.png"))
        self.player = Qt.QMediaPlayer()

    def mouseReleaseEvent(self, event: Qt.QMouseEvent):
        super().mouseReleaseEvent(event)

        file_name = self.dog_sound_1 if event.button() == Qt.Qt.LeftButton else self.dog_sound_2
        file_name = Qt.QUrl.fromLocalFile(file_name)
        self.player.setMedia(Qt.QMediaContent(file_name))
        self.player.play()


if __name__ == "__main__":
    app = Qt.QApplication([])

    w = Widget()
    w.show()

    app.exec()
