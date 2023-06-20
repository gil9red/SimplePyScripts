#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QProgressDialog
from PyQt5.QtCore import Qt

from .KeyValueLabel import KeyValueLabel


class FieldsProgressDialog(QProgressDialog):
    def __init__(
        self,
        minimum,
        maximum,
        window_title,
        label_text="Operation in progress...",
        parent=None,
    ):
        super().__init__(parent)

        self.setWindowModality(Qt.WindowModal)
        self.setRange(minimum, maximum)
        self.setWindowTitle(window_title)

        self._label = KeyValueLabel(self)
        self.setLabel(self._label)

        self.setLabelText(label_text)

    def setFields(self, fields: dict):
        self._label.setFields(fields)

        # NOTE: Для вызова внутреннего ensureSizeIsAtLeastSizeHint, без которого не будет
        #       обновлен размер progress dialog.
        #       https://code.woboq.org/qt5/qtbase/src/widgets/dialogs/qprogressdialog.cpp.html#387
        self.setLabelText("")
