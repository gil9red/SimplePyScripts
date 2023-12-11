#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import traceback
import sys

from pathlib import Path

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import Qt

from ui_main_window import Ui_MainWindow
from utils import get_filling_in_missing, xml_to_flatten_dict, json_to_flatten_dict


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


XML_STR = """
<mydocument has="an attribute">
  <and>
    <many>elements</many>
    <many>more elements</many>
  </and>
  <plus a="complex">element as well</plus>
</mydocument>
""".strip()
# TODO:
XML_STR = """
<mydocument has="an attribute2">
  <and>
    <many>elements</many>
    <many>more elements</many>
  </and>
  <plus>element as well</plus>
  <comment>Hello World!</comment>
</mydocument>
""".strip()

JSON_STR = """
{
    "mydocument": {
        "@has": "an attribute",
        "and": {
            "many": [
                "elements",
                "more elements"
            ]
        },
        "plus": {
            "@a": "complex",
            "#text": "element as well"
        }
    }
}
""".strip()
# TODO:
JSON_STR = """
{
    "mydocument": {
        "@has": "an attribute",
        "and": {
            "many": [
                "elements",
                "more elements"
            ]
        },
        "plus": {
            "@a": "complex",
            "#text": "element as well"
        },
        "comment": "Hello World!"
    }
}
""".strip()

# # TODO: наборы?
# JSON_STR = """
# <mydocument has="an attribute2">
#   <and>
#     <many>elements2</many>
#     <many>more elements</many>
#   </and>
#   <plus>element as well</plus>
#   <comment>Hello World!</comment>
#   <text>Hello World!</text>
# </mydocument>
# """.strip()


# TODO: Флаг для отображения только разных значений / ключей

# TODO: Выделить столбы поля. Мб жирнее сделать?
# TODO: ... или еще и цветом?
# TODO: Надо бы и поле заголовка выделить
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle(str(Path(__file__).parent.resolve().name))

        self.ui.push_button_diff.clicked.connect(self._do_diff)
        self.ui.cb_only_diff.clicked.connect(self._show_only_diff)

    def _add_row_to_table(self, *values):
        name1, value1, value2, name2 = values
        no_match = name1 != name2 or value1 != value2

        row = self.ui.table_widget.rowCount()
        self.ui.table_widget.setRowCount(row + 1)

        for i, value in enumerate(values):
            item = QTableWidgetItem(str(value))

            if not value:
                item.setText("<not defined>")
                item.setForeground(Qt.GlobalColor.gray)

            if no_match:
                item.setBackground(Qt.GlobalColor.red)

            # TODO:
            if i in (0, 3):
                f = item.font()
                f.setBold(True)
                item.setFont(f)

            item.setData(Qt.ItemDataRole.UserRole, no_match)

            self.ui.table_widget.setItem(row, i, item)

    def _do_diff(self):
        source_1 = self.ui.edit_source_1.toPlainText()
        source_2 = self.ui.edit_source_2.toPlainText()

        try:
            source_dict_1 = json_to_flatten_dict(source_1)
        except Exception:
            source_dict_1 = xml_to_flatten_dict(source_1)

        try:
            source_dict_2 = json_to_flatten_dict(source_2)
        except Exception:
            source_dict_2 = xml_to_flatten_dict(source_2)

        source_dict_filling_1, source_dict_filling_2 = get_filling_in_missing(
            list(source_dict_1.keys()), list(source_dict_2.keys())
        )

        # Clear
        while self.ui.table_widget.rowCount() > 0:
            self.ui.table_widget.removeRow(0)

        for key_1, key_2 in zip(source_dict_filling_1, source_dict_filling_2):
            self._add_row_to_table(
                key_1,
                source_dict_1.get(key_1, ""),
                source_dict_2.get(key_2, ""),
                key_2
            )

        self.ui.table_widget.resizeColumnsToContents()

        self._show_only_diff(self.ui.cb_only_diff.isChecked())

    def _show_only_diff(self, checked: bool):
        for row in range(self.ui.table_widget.rowCount()):
            no_match = self.ui.table_widget.item(row, 0).data(Qt.ItemDataRole.UserRole)

            if not checked or no_match:
                self.ui.table_widget.showRow(row)
            else:
                self.ui.table_widget.hideRow(row)


if __name__ == '__main__':
    app = QApplication([])
    
    mw = MainWindow()
    mw.ui.edit_source_1.setPlainText(XML_STR)
    mw.ui.edit_source_2.setPlainText(JSON_STR)

    mw.show()
    
    app.exec()
