#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QListView

from .ThumbnailDelegate import ThumbnailDelegate


class ListImagesWidget(QListView):
    def __init__(self, icon_width, icon_height, image_cache, file_name_index) -> None:
        super().__init__()

        self.setMovement(QListView.Static)
        self.setDragEnabled(False)
        self.setDragDropMode(QListView.NoDragDrop)
        self.setDropIndicatorShown(False)
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setSpacing(5)
        self.setUniformItemSizes(True)
        self.setItemDelegate(
            ThumbnailDelegate(
                self, icon_width, icon_height, image_cache, file_name_index
            )
        )
