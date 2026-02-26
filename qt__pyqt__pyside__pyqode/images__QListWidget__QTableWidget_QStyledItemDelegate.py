#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as dt
from glob import glob
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication,
    QListWidget,
    QListWidgetItem,
    QTableWidget,
    QTableWidgetItem,
    QStyledItemDelegate,
    QStyle,
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt


class ImageDelegate(QStyledItemDelegate):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

    def paint(self, painter, option, index) -> None:
        pixmap = index.data(Qt.DecorationRole)
        if pixmap:
            # pixmap = pixmap.scaled(
            #     option.rect.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            # )
            # painter.drawPixmap(option.rect, pixmap)
            painter.drawPixmap(option.rect.topLeft(), pixmap)

        # Чтобы при выделенной строке на картинке тоже было выделена рамка
        if option.state & QStyle.State_Selected:
            brush = option.palette.highlight()
            color = brush.color()
            color.setAlphaF(0.5)
            painter.fillRect(option.rect, color)


ICON_WIDTH = 128
ICON_HEIGHT = 128


if __name__ == "__main__":
    app = QApplication([])

    file_names = glob(r"D:\все фотки\**\*.jpg", recursive=True)
    print(f"Files: {len(file_names)}")

    list_widget = QListWidget()
    list_widget.setStyleSheet(
        """
        QListWidget::item {
            border: 1px solid gray;
        }
        QListWidget::item:selected {
            color: black;
            background-color: #0087BD;
        }
    """
    )
    list_widget.setMovement(QListWidget.Static)
    list_widget.setDragEnabled(False)
    list_widget.setDragDropMode(QListWidget.NoDragDrop)
    list_widget.setDropIndicatorShown(False)
    list_widget.setViewMode(QListWidget.IconMode)
    list_widget.setResizeMode(QListWidget.Adjust)
    list_widget.setIconSize(QSize(ICON_WIDTH, ICON_HEIGHT))
    list_widget.setSpacing(2)
    list_widget.setUniformItemSizes(True)
    list_widget.itemClicked.connect(lambda item: print(item.sizeHint()))
    list_widget.move(100, 50)
    list_widget.resize(800, 600)
    list_widget.show()

    headers = ["IMAGE", "FILE NAME", "DIRECTORY"]
    table_widget = QTableWidget()
    table_widget.setColumnCount(len(headers))
    table_widget.setHorizontalHeaderLabels(headers)
    table_widget.horizontalHeader().setStretchLastSection(True)
    table_widget.setColumnWidth(0, ICON_WIDTH)
    table_widget.setItemDelegateForColumn(0, ImageDelegate())
    table_widget.setIconSize(QSize(ICON_WIDTH, ICON_HEIGHT))
    table_widget.move(list_widget.pos().x(), list_widget.geometry().bottom())
    table_widget.resize(800, 600)
    table_widget.show()

    start_time = dt.datetime.now()
    row = 0

    for i, file_name in enumerate(file_names, 1):
        list_widget.setWindowTitle(
            f"{i} / {len(file_names)} ({i / len(file_names):.0%})"
        )
        table_widget.setWindowTitle(
            f"{i} / {len(file_names)} ({i / len(file_names):.0%})"
        )

        pixmap = QPixmap(file_name)
        if pixmap.isNull():
            continue

        pixmap = pixmap.scaled(
            ICON_WIDTH, ICON_WIDTH, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        base_file_name = Path(file_name).name

        item = QListWidgetItem(QIcon(pixmap), base_file_name)
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        item.setSizeHint(QSize(ICON_WIDTH, ICON_HEIGHT + 20))
        list_widget.addItem(item)

        table_widget.setRowCount(table_widget.rowCount() + 1)
        table_widget.setRowHeight(row, ICON_HEIGHT)
        item_img = QTableWidgetItem()
        item_img.setData(Qt.DecorationRole, pixmap)
        item_img.setSizeHint(QSize(ICON_WIDTH, ICON_HEIGHT))
        table_widget.setItem(row, 0, item_img)
        table_widget.setItem(row, 1, QTableWidgetItem(base_file_name))
        table_widget.setItem(row, 2, QTableWidgetItem(str(Path(file_name).parent)))
        row += 1

        QApplication.processEvents()

    list_widget.setWindowTitle(
        list_widget.windowTitle()
        + ". Elapsed: "
        + str(dt.datetime.now() - start_time).split(".")[0]
    )
    table_widget.setWindowTitle(
        table_widget.windowTitle()
        + ". Elapsed: "
        + str(dt.datetime.now() - start_time).split(".")[0]
    )

    app.exec()
