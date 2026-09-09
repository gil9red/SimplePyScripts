#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QStyle,
    QAbstractItemView,
)
from PyQt6.QtGui import QPainter, QPalette, QFontMetrics, QImage, QBrush
from PyQt6.QtCore import (
    Qt,
    QSize,
    QRect,
    QModelIndex,
    QThreadPool,
    QAbstractItemModel,
    pyqtSignal,
)

from .ThumbnailWorker import ThumbnailWorker
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
        width: int,
        height: int,
        image_cache: dict[str, QImage | None],
        file_name_index: int = 0,
    ) -> None:
        super().__init__()

        self.width: int = width
        self.height: int = height
        self.title_height: int = 20
        self.title_margin: int = 5
        self.view: QAbstractItemView = view
        self.image_cache: dict[str, QImage | None] = image_cache
        self.file_name_index: int = file_name_index

    def _on_about_image(
        self,
        file_name: str,
        image: QImage,
        index: QModelIndex,
    ) -> None:
        self.image_cache[file_name] = image
        self.view.update(index)

    def paint(
        self,
        painter: QPainter | None,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> None:
        if not painter:
            return

        model: QAbstractItemModel | None = index.model()
        if not model:
            return

        style: QStyle | None = (
            option.widget.style() if option.widget else QApplication.style()
        )
        if not style:
            return

        rect = option.rect
        self.initStyleOption(option, index)

        col_index = model.index(index.row(), self.file_name_index)

        file_name = model.data(col_index)
        base_file_name = Path(file_name).name
        font_metrics = QFontMetrics(painter.font())

        is_main = model.data(col_index, FileListModel.IsMainRole)
        is_matched = model.data(col_index, FileListModel.IsMatchedRole)

        # Draw correct background
        option.text = ""
        style.drawControl(
            QStyle.ControlElement.CE_ItemViewItem, option, painter, option.widget
        )

        cg = (
            QPalette.ColorGroup.Normal
            if option.state & QStyle.StateFlag.State_Enabled
            else QPalette.ColorGroup.Disabled
        )
        if cg == QPalette.ColorGroup.Normal and not (
            option.state & QStyle.StateFlag.State_Active
        ):
            cg = QPalette.ColorGroup.Inactive

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
        painter.setPen(option.palette.color(cg, QPalette.ColorRole.Text))
        elided_text = font_metrics.elidedText(
            base_file_name,
            Qt.TextElideMode.ElideRight,
            rect.width() - self.title_margin * 2,
        )
        painter.drawText(
            rect_title,
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
            elided_text,
        )
        painter.restore()

        if option.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(rect, get_half_alpha(option.palette.highlight()))
        elif option.state & QStyle.StateFlag.State_MouseOver:
            painter.fillRect(rect, get_half_alpha(option.palette.midlight()))

        painter.save()

        # Выделяем элементы
        if is_main or is_matched:
            pen = painter.pen()

            if is_main:
                pen.setWidth(pen.width() * 5)
                pen.setColor(Qt.GlobalColor.darkGreen)
                painter.setPen(pen)
            else:
                pen.setWidth(pen.width() * 3)
                pen.setColor(Qt.GlobalColor.green)
                painter.setPen(pen)

        painter.drawRect(rect)

        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        return QSize(self.width, self.height + self.title_height)
