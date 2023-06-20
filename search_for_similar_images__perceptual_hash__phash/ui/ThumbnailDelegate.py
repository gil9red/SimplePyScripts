#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QStyle,
    QAbstractItemView,
)
from PyQt5.QtGui import QPainter, QPalette, QFontMetrics, QImage, QBrush, QPen
from PyQt5.QtCore import Qt, QSize, QRect, QModelIndex, QThreadPool, pyqtSignal

sys.path.append(
    r"..\sqlite3__examples\view_many_images__lazy__delegates__async_load_images\utils"
)
from ThumbnailWorker import ThumbnailWorker

from .FileListModel import FileListModel


def get_half_alpha(brush: QBrush) -> QBrush:
    color = brush.color()
    color.setAlphaF(0.5)
    brush.setColor(color)
    return brush


class ThumbnailDelegate(QStyledItemDelegate):
    about_append_image = pyqtSignal(str)

    def __init__(
        self,
        view: QAbstractItemView,
        width,
        height,
        image_cache: dict,
        file_name_index=0,
    ):
        super().__init__()

        self.width = width
        self.height = height
        self.title_height = 20
        self.title_margin = 5
        self.view = view
        self.image_cache = image_cache
        self.file_name_index = file_name_index

    def _on_about_image(self, file_name: str, image: QImage, index: QModelIndex):
        self.image_cache[file_name] = image
        self.view.update(index)

    def paint(self, painter: QPainter, opt: QStyleOptionViewItem, index: QModelIndex):
        rect = opt.rect
        self.initStyleOption(opt, index)

        model = index.model()
        col_index = model.index(index.row(), self.file_name_index)

        file_name = model.data(col_index)
        base_file_name = Path(file_name).name
        font_metrics = QFontMetrics(painter.font())

        is_main = model.data(col_index, FileListModel.IsMainRole)
        is_matched = model.data(col_index, FileListModel.IsMatchedRole)

        # Draw correct background
        opt.text = ""
        style = opt.widget.style() if opt.widget else QApplication.style()
        style.drawControl(QStyle.CE_ItemViewItem, opt, painter, opt.widget)

        cg = QPalette.Normal if opt.state & QStyle.State_Enabled else QPalette.Disabled
        if cg == QPalette.Normal and not (opt.state & QStyle.State_Active):
            cg = QPalette.Inactive

        # # Set pen color
        # if opt.state & QStyle.State_Selected:
        #     painter.setPen(opt.palette.color(cg, QPalette.HighlightedText))
        # else:
        #     painter.setPen(opt.palette.color(cg, QPalette.Text))

        if file_name in self.image_cache:
            img = self.image_cache[file_name]
            if img and not img.isNull():
                painter.drawImage(
                    rect.topLeft(),
                    # QRect(rect.left(), rect.top(), rect.width(), rect.height() - self.title_height),
                    img,
                )
        else:
            self.image_cache[file_name] = None

            worker = ThumbnailWorker(file_name, self.width, self.height)
            worker.signals.about_image.connect(
                lambda file_name, image: self._on_about_image(file_name, image, index)
            )
            QThreadPool.globalInstance().start(worker)

        rect_title = QRect(rect.left(), rect.top(), rect.width(), rect.height())
        rect_title.setLeft(rect_title.left() + self.title_margin)
        rect_title.setTop(rect_title.top() + rect_title.height() - self.title_height)
        rect_title.setRight(rect_title.right() - self.title_margin)

        painter.save()
        painter.setPen(opt.palette.color(cg, QPalette.Text))
        elided_text = font_metrics.elidedText(
            base_file_name, Qt.ElideRight, rect.width() - self.title_margin * 2
        )
        painter.drawText(rect_title, Qt.AlignVCenter | Qt.AlignLeft, elided_text)
        painter.restore()

        if opt.state & QStyle.State_Selected:
            painter.fillRect(rect, get_half_alpha(opt.palette.highlight()))
        elif opt.state & QStyle.State_MouseOver:
            painter.fillRect(rect, get_half_alpha(opt.palette.midlight()))

        painter.save()

        # Выделяем элементы
        if is_main or is_matched:
            pen = painter.pen()

            if is_main:
                pen.setWidth(pen.width() * 5)
                pen.setColor(Qt.darkGreen)
                painter.setPen(pen)
            else:
                pen.setWidth(pen.width() * 3)
                pen.setColor(Qt.green)
                painter.setPen(pen)

        painter.drawRect(rect)

        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        return QSize(self.width, self.height + self.title_height)
