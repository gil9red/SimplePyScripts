#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random

from PySide.QtGui import *

from student import Student


DEFAULT_NAMES = [
    "Вася Пупкин",
    "Иван Иванов",
    "Катя Спилберг",
]

DEFAULT_GROUPS = [
    "Da-12",
    "Bg-1",
    "Aa-09",
]


class AddStudentDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add student dialog")

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.name = QLineEdit(random.choice(DEFAULT_NAMES))
        self.group = QLineEdit(random.choice(DEFAULT_GROUPS))

        self.layout = QFormLayout()
        self.layout.addRow("Name", self.name)
        self.layout.addRow("Group", self.group)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.layout)
        self.main_layout.addWidget(self.buttonBox)

        self.setLayout(self.main_layout)

        self.student = None

    def accept(self):
        super().accept()

        self.student = Student(self.name.text(), self.group.text())
