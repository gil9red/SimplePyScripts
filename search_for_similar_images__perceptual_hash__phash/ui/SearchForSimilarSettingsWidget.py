#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QWidget, QFormLayout, QComboBox, QSpinBox, QCheckBox
from PyQt5.QtCore import QSettings, pyqtSignal

from common import (
    IMAGE_HASH_ALGO,
    DEFAULT_IMAGE_HASH_ALGO,
    DEFAULT_IMAGE_HASH_MAX_SCORE,
)


class SearchForSimilarSettingsWidget(QWidget):
    about_mark_matching = pyqtSignal(bool)

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Search for similar")

        self.cb_algo = QComboBox()
        self.cb_algo.addItems(IMAGE_HASH_ALGO)

        self.sb_max_score = QSpinBox()

        self.cb_mark_matching = QCheckBox()
        self.cb_mark_matching.clicked.connect(self.about_mark_matching)

        layout = QFormLayout()
        layout.addRow("Hash algo:", self.cb_algo)
        layout.addRow("Max score:", self.sb_max_score)
        layout.addRow("Mark matching:", self.cb_mark_matching)

        self.setLayout(layout)

    def read_settings(self, ini: QSettings) -> None:
        ini.beginGroup(self.__class__.__name__)

        self.cb_algo.setCurrentText(ini.value("algo", DEFAULT_IMAGE_HASH_ALGO))
        self.sb_max_score.setValue(
            int(ini.value("max_score", DEFAULT_IMAGE_HASH_MAX_SCORE))
        )
        self.cb_mark_matching.setChecked(ini.value("mark_matching", "true") == "true")

        ini.endGroup()

    def write_settings(self, ini: QSettings) -> None:
        ini.beginGroup(self.__class__.__name__)

        ini.setValue("algo", self.cb_algo.currentText())
        ini.setValue("max_score", self.sb_max_score.value())
        ini.setValue("mark_matching", self.cb_mark_matching.isChecked())

        ini.endGroup()
