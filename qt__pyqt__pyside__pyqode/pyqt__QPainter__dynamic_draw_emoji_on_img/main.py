#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import traceback
import sys

from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
    QButtonGroup,
    QAbstractButton,
    QMessageBox,
)
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt, QRectF


# Для отлова всех исключений, которые в слотах Qt могут "затеряться" и привести к тихому падению
def log_uncaught_exceptions(ex_cls, ex, tb) -> None:
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print("Error: ", text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


DIR: Path = Path(__file__).parent.resolve()
FILE_NAME_IMAGE: str = str(DIR / "favicon.png")


def draw_text_to_bottom_right(img: QPixmap, text: str, scale_text_from_img: float = 0.5) -> None:
    p = QPainter(img)

    factor = (img.width() * scale_text_from_img) / p.fontMetrics().width(text)
    if factor < 1 or factor > 1.25:
        f = p.font()
        point_size = f.pointSizeF() * factor
        if point_size > 0:
            f.setPointSizeF(point_size)
            p.setFont(f)

    # Bottom + right
    text_rect = p.fontMetrics().boundingRect(text)
    rect = QRectF(
        img.width() - text_rect.width(),
        img.height() - text_rect.height(),
        img.width(),
        img.height(),
    )

    p.drawText(rect, text)

    p = None  # NOTE: Иначе, почему-то будет ошибка


class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.img_view = QLabel()
        self.img_view.setAlignment(Qt.AlignCenter)
        self.img_view.setFrameStyle(QLabel.Box)
        self._update_img_view(QPixmap(FILE_NAME_IMAGE))

        self.button_group = QButtonGroup()
        self.button_group.addButton(QPushButton("🔄", parent=self))
        self.button_group.addButton(QPushButton("⚠️", parent=self))
        self.button_group.addButton(QPushButton("💰", parent=self))
        self.button_group.buttonClicked.connect(self._on_button_clicked)

        buttons_layout = QHBoxLayout()
        for b in self.button_group.buttons():
            buttons_layout.addWidget(b)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.img_view)
        main_layout.addLayout(buttons_layout)

    def _update_img_view(self, img: QPixmap) -> None:
        self.img_view.setPixmap(img)
        self.img_view.setMinimumSize(img.size() * 1.1)

    def _on_button_clicked(self, button: QAbstractButton) -> None:
        text = button.text()
        img = QPixmap(FILE_NAME_IMAGE)
        draw_text_to_bottom_right(img, text)

        self._update_img_view(img)


if __name__ == "__main__":
    app = QApplication([])

    w = Window()
    w.show()

    app.exec()
