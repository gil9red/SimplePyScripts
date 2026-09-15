#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QListView
from PyQt6.QtCore import Qt, QModelIndex

from .ThumbnailDelegate import ThumbnailDelegate


class ListImagesWidget(QListView):
    def __init__(
        self,
        icon_width: int,
        icon_height: int,
        image_cache: dict[str, QImage],
        file_name_index: int,
    ) -> None:
        super().__init__()

        self.image_cache: dict[str, QImage] = image_cache

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
                self, icon_width, icon_height, self.image_cache, file_name_index
            )
        )

    def currentFileName(self) -> str | None:
        index = self.currentIndex()
        if not index.isValid():
            return None

        return index.data(Qt.ItemDataRole.DisplayRole)

    def removeFromList(self, file_name: str) -> None:
        model = self.model()

        found_indexes: list[QModelIndex] = model.match(
            model.index(0, 0),
            Qt.ItemDataRole.DisplayRole,
            file_name,
            1,  # hits
            Qt.MatchFlag.MatchExactly,
        )
        if found_indexes:
            target_index: QModelIndex = found_indexes[0]
            model.removeRow(target_index.row())

            file_name = target_index.data(Qt.ItemDataRole.DisplayRole)
            if file_name in self.image_cache:
                self.image_cache.pop(file_name)
