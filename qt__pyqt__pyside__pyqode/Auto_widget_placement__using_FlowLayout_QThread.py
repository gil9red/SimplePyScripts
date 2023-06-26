#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "ipetrash"


import random
import sys
import time
import traceback

from PyQt5.QtWidgets import (
    QWidget,
    QMessageBox,
    QVBoxLayout,
    QApplication,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
)
from PyQt5.QtGui import QPainter, QImage, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from FlowLayout import FlowLayout


# Для отлова всех исключений, которые в слотах Qt могут "затеряться" и привести к тихому падению
def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print("Error: ", text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


def seconds_to_str(seconds: int) -> str:
    hh, mm = divmod(seconds, 3600)
    mm, ss = divmod(mm, 60)
    return "%02d:%02d:%02d" % (hh, mm, ss)


class ImgThread(QThread):
    new_img = pyqtSignal(QImage)

    def __init__(self, life_time_seconds=60):
        super().__init__()

        self.life_time_seconds = life_time_seconds

    def run(self):
        painter = QPainter()
        painter.setRenderHint(QPainter.Antialiasing)

        life_time_seconds = self.life_time_seconds

        while life_time_seconds > 0:
            life_time_seconds -= 1
            text = seconds_to_str(life_time_seconds)

            img = QImage(320, 240, QImage.Format_ARGB32)
            img.fill(Qt.white)

            painter.begin(img)

            # Рисование рамки вокруг картинки
            border_rect = img.rect()
            border_rect.setWidth(border_rect.width() - 1)
            border_rect.setHeight(border_rect.height() - 1)
            painter.drawRect(border_rect)

            try:
                # Алгоритм изменения размера текста взят из http://stackoverflow.com/a/2204501
                # Для текущего пришлось немного адаптировать
                factor = (
                    img.width() / painter.fontMetrics().width(text) / 1.5
                )  # Ширина текста 2/3 от ширины
                if factor < 1 or factor > 1.25:
                    f = painter.font()
                    point_size = f.pointSizeF() * factor
                    if point_size > 0:
                        f.setPointSizeF(point_size)
                        painter.setFont(f)

                painter.drawText(img.rect(), Qt.AlignCenter, text)

            finally:
                painter.end()

            self.new_img.emit(img.copy())

            time.sleep(1)


class ImgWidget(QWidget):
    closed = pyqtSignal()

    def __init__(self, life_time_seconds=60):
        super().__init__()

        self._thread = ImgThread(life_time_seconds)
        self._thread.new_img.connect(self._on_new_img)
        self._thread.finished.connect(self.close)
        self._thread.start()

        self._label = QLabel()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._label)

        self.setLayout(layout)

    def _on_new_img(self, img: QImage):
        if not img:
            return

        self.setFixedSize(img.size())
        self._label.setPixmap(QPixmap.fromImage(img))

    def closeEvent(self, event):
        self.closed.emit()

        super().closeEvent(event)


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(__file__.split("/")[-1])

        button = QPushButton("Add")
        button.clicked.connect(self._on_push_add)

        self.items_layout = FlowLayout()

        scroll_area = QScrollArea()
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(QWidget())
        scroll_area.widget().setLayout(self.items_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(button)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def _on_push_add(self):
        w = ImgWidget(life_time_seconds=random.randint(10, 100))
        w.closed.connect(lambda w=w: self.items_layout.removeWidget(w))

        self.items_layout.addWidget(w)


if __name__ == "__main__":
    app = QApplication([])

    mw = Window()
    mw.resize(900, 600)
    mw.show()

    app.exec()
