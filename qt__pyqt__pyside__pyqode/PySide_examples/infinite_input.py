#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PySide.QtGui import *
from PySide.QtCore import *


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.line_edit_list = list()

        self._add_line_edit()

    def _add_line_edit(self):
        line_edit = QLineEdit()
        line_edit.textEdited.connect(self._text_edited)

        self.layout.addWidget(line_edit)
        self.line_edit_list.append(line_edit)

    def _text_edited(self, text):
        if not self.line_edit_list:
            return

        if self.line_edit_list[-1] == self.sender() and text:
            self._add_line_edit()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    w = Widget()
    w.show()

    sys.exit(app.exec_())
