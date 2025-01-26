#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback

import cydoomgeneric as cdg
import numpy as np

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPainter, QKeyEvent, QPaintEvent
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}\n"
    text += "".join(traceback.format_tb(tb))
    print(text)

    if isinstance(ex, KeyboardInterrupt):
        QApplication.instance().quit()
        return

    if QApplication.instance():
        msg_box = QMessageBox(
            QMessageBox.Critical,
            "Ошибка",
            f"Ошибка: {ex}",
        )
        msg_box.setDetailedText(text)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()


sys.excepthook = log_uncaught_exceptions


def numpy_array_to_QImage(numpy_array: np.ndarray) -> QImage:
    height, width = numpy_array.shape[:2]
    data: bytes = numpy_array.data.tobytes()

    return QImage(
        data,
        width,
        height,
        QImage.Format_RGB32,
    )


def get_key(event: QKeyEvent) -> int | None:
    if event.modifiers() & Qt.ControlModifier:
        return cdg.Keys.RCTRL

    if event.modifiers() & Qt.ShiftModifier:
        return cdg.Keys.RSHIFT

    if event.modifiers() & Qt.AltModifier:
        return cdg.Keys.LALT

    match event.key():
        case Qt.Key_W | Qt.Key_Up:
            return cdg.Keys.UPARROW
        case Qt.Key_A:
            return cdg.Keys.STRAFE_L
        case Qt.Key_D:
            return cdg.Keys.STRAFE_R
        case Qt.Key_S | Qt.Key_Down:
            return cdg.Keys.DOWNARROW
        case Qt.Key_Left:
            return cdg.Keys.LEFTARROW
        case Qt.Key_Right:
            return cdg.Keys.RIGHTARROW
        case Qt.Key_E:
            return cdg.Keys.USE
        case Qt.Key_Space:
            return cdg.Keys.FIRE
        case Qt.Key_Return:
            return cdg.Keys.ENTER
        case Qt.Key_Escape:
            return cdg.Keys.ESCAPE


KEY_PRESSED: dict[int, bool] = dict()


class CyDoomGenericThread(QThread):
    about_draw_frame = pyqtSignal(np.ndarray)
    about_set_window_title = pyqtSignal(str)

    def __init__(
        self,
        path_wad: str,
        width: int,
        height: int,
    ):
        super().__init__()

        self.path_wad = path_wad
        self.width = width
        self.height = height

    def get_key(self) -> tuple[int, int] | None:
        if not KEY_PRESSED:
            return

        key, is_pressed = KEY_PRESSED.popitem()
        return int(is_pressed), key

    def run(self):
        cdg.init(
            self.width,
            self.height,
            draw_frame=self.about_draw_frame.emit,
            get_key=self.get_key,
            set_window_title=self.about_set_window_title.emit,
        )
        cdg.main(argv=["cydoomgeneric", "-iwad", self.path_wad])


class WidgetDoom(QWidget):
    def __init__(self, path_wad: str):
        super().__init__()

        self._resx = 640
        self._resy = 400

        self.thread_engine = CyDoomGenericThread(
            path_wad=path_wad,
            width=self._resx,
            height=self._resy,
        )
        self.thread_engine.about_draw_frame.connect(self.draw_frame)
        self.thread_engine.about_set_window_title.connect(self.setWindowTitle)
        # TODO:
        # self.thread_engine.finished.connect(self.close)
        self.thread_engine.start()

        self.img: QImage | None = None

        self.setFixedSize(self._resx, self._resy)

    def draw_frame(self, pixels: np.ndarray):
        self.img = numpy_array_to_QImage(pixels)
        self.update()

    def keyPressEvent(self, event: QKeyEvent):
        key = get_key(event)
        if key is not None:
            KEY_PRESSED[key] = True

    def keyReleaseEvent(self, event: QKeyEvent):
        key = get_key(event)
        if key is not None:
            KEY_PRESSED[key] = False

    def paintEvent(self, event: QPaintEvent):
        if not self.img:
            return

        p = QPainter(self)
        p.drawImage(0, 0, self.img)


if __name__ == "__main__":
    from pathlib import Path

    path_wad = str(Path(__file__).parent.resolve() / "DOOM1.WAD")

    app = QApplication([])

    g = WidgetDoom(path_wad=path_wad)
    g.show()

    app.exec()
