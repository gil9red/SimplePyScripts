#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import itertools
from collections import defaultdict

from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QProgressBar,
    QHeaderView,
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread

import imagehash


class CrossSearchSimilarImagesThread(QThread):
    about_found_similars = pyqtSignal(str, list)

    def __init__(
        self, image_by_hashes: dict = None, hash_algo: str = None, max_score: int = None
    ) -> None:
        super().__init__()

        self.image_by_hashes = image_by_hashes
        self.hash_algo = hash_algo
        self.max_score = max_score

    def run(self) -> None:
        img_by_hash = dict()
        for file_name, hashes in self.image_by_hashes.items():
            hash_value = hashes[self.hash_algo]

            # TODO: Monkey patch. https://github.com/JohannesBuchner/imagehash/issues/112
            if self.hash_algo == "colorhash":
                from PIL import Image

                hash_value = imagehash.colorhash(Image.open(file_name))

            img_by_hash[file_name] = hash_value

        file_name_by_similars = defaultdict(list)
        for img_1, img_2 in itertools.product(img_by_hash.items(), repeat=2):
            if img_1 == img_2:
                continue

            file_name_1, hash_img_1 = img_1
            file_name_2, hash_img_2 = img_2

            score = hash_img_1 - hash_img_2
            if score > self.max_score:
                continue

            file_name_by_similars[file_name_1].append((file_name_2, score))

        # Обратная сортировка по количеству элементов, а названия элементов сортируются по возрастанию
        items = sorted(file_name_by_similars.items(), key=lambda x: (-len(x[1]), x[0]))
        for file_name, similars in items:
            if not similars:
                continue

            self.about_found_similars.emit(file_name, similars)


class CrossSearchSimilarImagesDialog(QDialog):
    itemDoubleClicked = pyqtSignal(str)

    window_title = "Cross search similar images"

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle(self.window_title)
        self.resize(600, 600)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["FILE NAME", "SCORE"])
        self.tree_widget.header().setSectionResizeMode(1, QHeaderView.Fixed)
        self.tree_widget.header().resizeSection(0, 450)
        self.tree_widget.header().resizeSection(1, 75)
        self.tree_widget.setAlternatingRowColors(True)
        self.tree_widget.setExpandsOnDoubleClick(False)
        self.tree_widget.itemDoubleClicked.connect(
            lambda item, _: self.itemDoubleClicked.emit(item.data(0, Qt.UserRole))
        )

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()

        self.thread = CrossSearchSimilarImagesThread()
        self.thread.started.connect(lambda: self.progress_bar.show())
        self.thread.finished.connect(lambda: self.progress_bar.hide())
        self.thread.about_found_similars.connect(self._on_about_found_similars)

        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.tree_widget)
        self.setLayout(layout)

    def _on_about_found_similars(self, file_name: str, similars: list[str]) -> None:
        item = QTreeWidgetItem([f"{file_name} ({len(similars)})"])
        item.setData(0, Qt.UserRole, file_name)

        self.tree_widget.addTopLevelItem(item)

        for x, score in similars:
            child = QTreeWidgetItem([x, str(score)])
            child.setData(0, Qt.UserRole, x)
            item.addChild(child)

    def start(self, image_by_hashes: dict, hash_algo: str, max_score: int) -> None:
        self.setWindowTitle(
            f"{self.window_title}. hash_algo={hash_algo} max_score={max_score}"
        )
        self.tree_widget.clear()

        self.thread.image_by_hashes = image_by_hashes
        self.thread.hash_algo = hash_algo
        self.thread.max_score = max_score
        self.thread.start()

        self.show()
