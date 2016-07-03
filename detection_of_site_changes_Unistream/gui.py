#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Скрипт создает окно, позволяющее просматривать все ревизии и их различие."""


import sys

from PySide.QtGui import *
from PySide.QtCore import *

from main import session, TextRevision


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('detection_of_site_changes_Unistream')

        self.revision_list_widget = QListWidget()
        self.revision_list_widget.itemDoubleClicked.connect(self._show_last_diff)

        text_revisions = session.query(TextRevision).all()
        for rev in text_revisions:
            item = QListWidgetItem()
            item.setText(str(rev))
            item.setData(Qt.UserRole, rev)
            self.revision_list_widget.addItem(item)

        self.setCentralWidget(self.revision_list_widget)

    def _show_last_diff(self, item):
        row = self.revision_list_widget.row(item)

        file_name_a = 'file_a'
        file_name_b = 'file_b'

        file_a_text = self.revision_list_widget.item(row - 1).data(Qt.UserRole).text if row > 0 else ''
        file_b_text = self.revision_list_widget.item(row).data(Qt.UserRole).text

        with open(file_name_a, mode='w', encoding='utf-8') as f:
            f.write(file_a_text)

        with open(file_name_b, mode='w', encoding='utf-8') as f:
            f.write(file_b_text)

        import os
        os.system('kdiff3 {} {}'.format(file_name_a, file_name_b))

        if os.path.exists(file_name_a):
            os.remove(file_name_a)

        if os.path.exists(file_name_b):
            os.remove(file_name_b)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.resize(660, 300)
    mw.show()

    app.exec_()
