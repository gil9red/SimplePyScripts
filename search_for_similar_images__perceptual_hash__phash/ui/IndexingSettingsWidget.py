#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit
from PyQt5.QtCore import QSettings

from ui.SelectDirBox import SelectDirBox

from common import USER_PICTURES_DIR, DEFAULT_SUFFIXES


class IndexingSettingsWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Indexing")

        self.dir_box = SelectDirBox(visible_label=False)
        self.line_edit_suffixes = QLineEdit()

        layout = QFormLayout()
        layout.addRow("Directory:", self.dir_box)
        layout.addRow("Suffixes:", self.line_edit_suffixes)

        self.setLayout(layout)

    def read_settings(self, ini: QSettings) -> None:
        ini.beginGroup(self.__class__.__name__)

        self.dir_box.setValue(ini.value("dir_box", USER_PICTURES_DIR))
        self.line_edit_suffixes.setText(ini.value("suffixes", DEFAULT_SUFFIXES))

        ini.endGroup()

    def write_settings(self, ini: QSettings) -> None:
        ini.beginGroup(self.__class__.__name__)

        ini.setValue("dir_box", self.dir_box.getValue())
        ini.setValue("suffixes", self.line_edit_suffixes.text())

        ini.endGroup()
