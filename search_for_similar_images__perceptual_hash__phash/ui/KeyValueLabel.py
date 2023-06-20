#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QLabel, QFormLayout


class KeyValueLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._field_by_row = dict()
        self._layout = QFormLayout()
        self.setLayout(self._layout)

        self.setMinimumSize(200, 150)

    def setFields(self, fields: dict):
        while not self._layout.isEmpty():
            self._layout.takeAt(0)

        for label, field in self._field_by_row.values():
            label.hide()
            field.hide()

        for field_title, value in fields.items():
            value = str(value)

            if field_title in self._field_by_row:
                label_widget, field_widget = self._field_by_row[field_title]
                label_widget.show()
                field_widget.show()

            else:
                label_widget = QLabel(field_title + ":")
                font = label_widget.font()
                font.setBold(True)
                label_widget.setFont(font)

                field_widget = QLabel()
                self._field_by_row[field_title] = (label_widget, field_widget)

            field_widget.setText(value)

            self._layout.addRow(label_widget, field_widget)

    def sizeHint(self):
        return self._layout.sizeHint()


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])

    label = KeyValueLabel()
    label.setFields(
        {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
        }
    )
    label.show()

    label.setFields(
        {
            "a": 1,
            "d": 4,
        }
    )
    label.setFields(
        {
            "abc": 123,
            "x": 2**3,
        }
    )

    app.exec()
