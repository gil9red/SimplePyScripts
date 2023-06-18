#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import time

from pathlib import Path

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt

from print__hprof_or_big_size_file import find_files_by_dirs, DIRS


if __name__ == "__main__":
    app = QApplication([])

    while True:
        result = find_files_by_dirs(DIRS)
        if not result:
            continue

        text = f"Files .hprof ({len(result)}):\n" + "\n".join(result)

        msg_box = QMessageBox(QMessageBox.Information, "Found .hprof!", text)
        msg_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
        remove_all_files_button = msg_box.addButton(
            "Remove all files", QMessageBox.DestructiveRole
        )
        msg_box.addButton(QMessageBox.Ok)
        msg_box.exec()

        if msg_box.clickedButton() == remove_all_files_button:
            for file_name in result:
                # "C:\DEV\trunk\java_pid12636.hprof" 6.1 GB (6603419857 bytes) -> C:\DEV\trunk\java_pid12636.hprof
                m = re.search('"(.+?)"', file_name)
                if m:
                    file_name = m.group(1)

                try:
                    Path(file_name).unlink()
                except Exception as e:
                    QMessageBox.warning(
                        None, "Warning", f"Error while removed {file_name!r}: {e}"
                    )

        time.sleep(5 * 60 * 60)
