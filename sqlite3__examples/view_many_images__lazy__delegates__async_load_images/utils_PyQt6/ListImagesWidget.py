#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QListView
from PyQt6.QtCore import Qt

from .ThumbnailDelegate import ThumbnailDelegate


class ListImagesWidget(QListView):
    def __init__(
        self,
        icon_width: int,
        icon_height: int,
        image_cache: dict[str, QImage | None],
        file_name_index: int,
    ) -> None:
        super().__init__()

        self.setMovement(QListView.Movement.Static)
        self.setDragEnabled(False)
        self.setDragDropMode(QListView.DragDropMode.NoDragDrop)
        self.setDropIndicatorShown(False)
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setSpacing(5)
        self.setUniformItemSizes(True)
        self.setItemDelegate(
            ThumbnailDelegate(
                self, icon_width, icon_height, image_cache, file_name_index
            )
        )

    def currentFileName(self) -> str | None:
        index = self.currentIndex()
        if not index.isValid():
            return None

        return index.data(Qt.ItemDataRole.DisplayRole)
