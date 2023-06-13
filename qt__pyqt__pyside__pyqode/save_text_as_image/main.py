#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback

from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QLineEdit,
    QFileDialog,
    QFontComboBox,
    QFormLayout,
    QMessageBox,
)
from PyQt5.QtGui import QPixmap, QPainter, QFontMetrics, QImageWriter
from PyQt5.QtCore import Qt


DIR = Path(__file__).parent


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(DIR.name)

        self.cb_font = QFontComboBox()
        self.cb_font.currentFontChanged.connect(self.render_image)

        self.sb_width = QSpinBox()
        self.sb_width.setRange(1, 4096)
        self.sb_width.setValue(600)
        self.sb_width.valueChanged.connect(self.render_image)

        self.text_edit = QLineEdit(text)
        self.text_edit.textChanged.connect(self.render_image)

        self.result_label = QLabel()

        self.pb_save_as = QPushButton('Сохранить как...')
        self.pb_save_as.clicked.connect(self._on_save_as)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.result_label)

        form_layout = QFormLayout()
        form_layout.addRow('Шрифт:', self.cb_font)
        form_layout.addRow('Ширина (px):', self.sb_width)
        form_layout.addRow('Текст:', self.text_edit)
        form_layout.addRow('Результат:', self.scroll)
        form_layout.addWidget(self.pb_save_as)

        self.setLayout(form_layout)

    def _on_save_as(self):
        # Список строк с поддерживаемыми форматами изображений
        formats = [str(x, encoding="utf-8") for x in QImageWriter.supportedImageFormats()]

        # Описываем как фильтры диалога
        filters = ["{} ( *.{} )".format(x.upper(), x) for x in formats]
        default_filter = "{} ( *.{} )".format('PNG', 'png')

        # Получим путь к файлу
        file_name = QFileDialog.getSaveFileName(self, None, None, '\n'.join(filters), default_filter)[0]
        if file_name:
            self.result_label.pixmap().save(file_name)

    def render_image(self):
        font = self.cb_font.currentFont()
        need_width = self.sb_width.value()
        text = self.text_edit.text()

        font_metrics = QFontMetrics(font)

        factor = need_width / font_metrics.width(text)
        if factor < 1 or factor > 1.25:
            point_size = font.pointSizeF() * factor
            if point_size > 0:
                font.setPointSizeF(point_size)

        font_metrics = QFontMetrics(font)
        text_rect = font_metrics.boundingRect(text)

        pix = QPixmap(text_rect.size())
        pix.fill(Qt.transparent)

        p = QPainter(pix)
        p.setRenderHint(QPainter.Antialiasing)
        p.setFont(font)
        p.setBrush(Qt.black)
        p.drawText(abs(text_rect.left()), abs(text_rect.top()), text)
        p.end()

        self.result_label.setPixmap(pix)


if __name__ == "__main__":
    app = QApplication([])

    text = "របាយការណ៍ប័ណ្ណឥណទាន"

    mw = MainWindow()
    mw.resize(800, 400)
    mw.show()

    mw.text_edit.setText(text)
    mw.render_image()

    app.exec_()
