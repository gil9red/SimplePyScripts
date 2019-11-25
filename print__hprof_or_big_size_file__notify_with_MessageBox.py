#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
from PyQt5.QtWidgets import QApplication, QMessageBox

from print__hprof_or_big_size_file import find_files_by_dirs, DIRS


if __name__ == '__main__':
    app = QApplication([])

    while True:
        result = find_files_by_dirs(DIRS)
        if result:
            QMessageBox.warning(None, 'Warn', '\n'.join(result))

        time.sleep(5 * 60 * 60)
