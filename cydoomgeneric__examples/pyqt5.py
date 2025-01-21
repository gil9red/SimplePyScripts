#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback
from queue import Queue
from typing import Optional

import numpy as np
import pygame

import cydoomgeneric as cdg

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, qRgb, QPainter
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


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/01558c1d6e01c88e93c0f1f82e3da0cd3a654a71/opencv__Color_Detection_Tool/main.py#L50-L89
GRAY_COLOR_TABLE = [qRgb(i, i, i) for i in range(256)]


def numpy_array_to_QImage(numpy_array: np.ndarray) -> QImage | None:
    if numpy_array.dtype != np.uint8:
        return

    height, width = numpy_array.shape[:2]
    data: bytes = numpy_array.data.tobytes()

    if len(numpy_array.shape) == 2:
        img = QImage(
            data,
            width,
            height,
            # numpy_array.strides[0],
            QImage.Format_Indexed8,
        )
        img.setColorTable(GRAY_COLOR_TABLE)
        return img

    elif len(numpy_array.shape) == 3:
        if numpy_array.shape[2] == 3:
            img = QImage(
                data,
                width,
                height,
                # numpy_array.strides[0],
                QImage.Format_RGB888,
            )
            return img

        elif numpy_array.shape[2] == 4:
            img = QImage(
                data,
                width,
                height,
                # numpy_array.strides[0],
                QImage.Format_ARGB32,
            )
            return img


# TODO:
keymap = {
    Qt.Key_Left: cdg.Keys.LEFTARROW,
    Qt.Key_Right: cdg.Keys.RIGHTARROW,
    Qt.Key_Up: cdg.Keys.UPARROW,
    Qt.Key_Down: cdg.Keys.DOWNARROW,
    pygame.K_COMMA: cdg.Keys.STRAFE_L,# TODO:
    pygame.K_PERIOD: cdg.Keys.STRAFE_R,# TODO:
    pygame.K_LCTRL: cdg.Keys.FIRE,# TODO:
    Qt.Key_Space: cdg.Keys.USE,
    pygame.K_RSHIFT: cdg.Keys.RSHIFT,# TODO:
    Qt.Key_Return: cdg.Keys.ENTER,
    # Qt.Key_Escape: cdg.Keys.ESCAPE,
}


class CyDoomGenericThread(QThread):
    about_draw_frame = pyqtSignal(np.ndarray)
    about_set_window_title = pyqtSignal(str)

    def __init__(self, width: int, height: int, queue: Queue):
        super().__init__()

        self.width = width
        self.height = height
        self.queue = queue

    def get_key(self) -> tuple[int, int] | None:
        try:
            state, key = self.queue.get_nowait()
            if key:
                return state, key
        except:
            pass

        return None

    def run(self):
        cdg.init(
            self.width,
            self.height,
            draw_frame=self.about_draw_frame.emit,
            get_key=self.get_key,
            set_window_title=self.about_set_window_title.emit,
        )
        cdg.main(argv=["cydoomgeneric", "-iwad", "DOOM1.WAD"])


class WidgetDoom(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self._resx = 640
        self._resy = 400
        self.q = Queue()

        self.thread_engine = CyDoomGenericThread(self._resx, self._resy, self.q)
        self.thread_engine.about_draw_frame.connect(self.draw_frame)
        self.thread_engine.about_set_window_title.connect(self.setWindowTitle)
        self.thread_engine.start()

        self.img: QImage | None = None

        # self.setFixedSize(self._resx, self._resy)
        self.resize(self._resx, self._resy)

    def draw_frame(self, pixels: np.ndarray):
        self.img = numpy_array_to_QImage(pixels)

        self.img.save("frame.jpg")
        self.img = QImage("frame.jpg")

        self.update()
        # QApplication.processEvents()

    # def get_key(self) -> tuple[int, int] | None:
    #     # for event in pygame.event.get():
    #     #     if event.type == pygame.QUIT:
    #     #         sys.exit()
    #     #
    #     #     if event.type == pygame.KEYDOWN:
    #     #         if event.key in keymap:
    #     #             return 1, keymap[event.key]
    #     #
    #     #     if event.type == pygame.KEYUP:
    #     #         if event.key in keymap:
    #     #             return 0, keymap[event.key]
    #     #
    #     return None

    # TODO:
    def _get_key(self, event):
        if event.modifiers() & Qt.ControlModifier:
            return cdg.Keys.RCTRL

        if event.modifiers() & Qt.ShiftModifier:
            return cdg.Keys.RSHIFT

        if event.modifiers() & Qt.AltModifier:
            return cdg.Keys.LALT
            # TODO:
            # return cdg.Keys.RALT

        match event.key():
            case Qt.Key_W: return cdg.Keys.UPARROW
            case Qt.Key_A: return cdg.Keys.LEFTARROW
            case Qt.Key_D: return cdg.Keys.RIGHTARROW
            case Qt.Key_S: return cdg.Keys.DOWNARROW
            case Qt.Key_E: return cdg.Keys.USE
            case Qt.Key_Space: return cdg.Keys.FIRE
            case Qt.Key_Return: return cdg.Keys.ENTER
        """
        pygame.K_COMMA: cdg.Keys.STRAFE_L,  # TODO:
        pygame.K_PERIOD: cdg.Keys.STRAFE_R,  # TODO:
        """

    # TODO:
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

        self.q.put((1, self._get_key(event)))

        # super().keyPressEvent(event)

    # TODO:
    def keyReleaseEvent(self, event):
        self.q.put((0, self._get_key(event)))

        # super().keyReleaseEvent(event)

    # def set_window_title(self, t: str) -> None:
    #     self.setWindowTitle(t)

    # TODO:
    def paintEvent(self, event):
        if not self.img:
            return

        p = QPainter(self)
        p.drawImage(0, 0, self.img)
        # print(self.img)
        # self.img.save("frame.jpg")


if __name__ == "__main__":
    app = QApplication([])

    g = WidgetDoom()
    g.show()

    app.exec()
