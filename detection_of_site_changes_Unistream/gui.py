#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Скрипт создает окно, позволяющее просматривать все ревизии и их различие."""


import os
import sys

from PySide.QtGui import *
from PySide.QtCore import *

from collections import defaultdict

from main import session, TextRevision

# TODO: возможность удаления записи
# TODO: возможность ручного запуска проверки


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("detection_of_site_changes_Unistream")

        self.revision_list_widget = QListWidget()
        self.revision_list_widget.itemDoubleClicked.connect(self._show_last_diff)

        # Словарь в ключе содержит хеш ревизии, а в значении -- список элементов ревизий
        text_hash_by_group_revisions_dict = defaultdict(list)

        text_revisions = session.query(TextRevision).all()
        for rev in text_revisions:
            item = QListWidgetItem()
            item.setText(str(rev))
            item.setData(Qt.UserRole, rev)

            text_hash_by_group_revisions_dict[rev.text_hash].append(item)
            self.revision_list_widget.addItem(item)

        # TODO: возможны коллизии по первым 6-символам
        # TODO: учитывать, что может получиться слишком светлый или темный фон
        for text_hash, items in text_hash_by_group_revisions_dict.items():
            if len(items) > 1:
                for item in items:
                    # Придаем элементу ревизии цвет, зависящий от первых 6-ти символов его хеша
                    color = QColor("#" + text_hash[:6])
                    item.setBackground(color)

        self.setCentralWidget(self.revision_list_widget)

    def _show_last_diff(self, item):
        row = self.revision_list_widget.row(item)

        file_name_a = "file_a"
        file_name_b = "file_b"

        file_a_text = (
            self.revision_list_widget.item(row - 1).data(Qt.UserRole).text
            if row > 0
            else ""
        )
        file_b_text = self.revision_list_widget.item(row).data(Qt.UserRole).text

        with open(file_name_a, mode="w", encoding="utf-8") as f:
            f.write(file_a_text)

        with open(file_name_b, mode="w", encoding="utf-8") as f:
            f.write(file_b_text)

        os.system(f"kdiff3 {file_name_a} {file_name_b}")

        if os.path.exists(file_name_a):
            os.remove(file_name_a)

        if os.path.exists(file_name_b):
            os.remove(file_name_b)


# TODO: выделять одинаковые элементы одним цветом
if __name__ == "__main__":
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.resize(660, 300)
    mw.show()

    app.exec_()
