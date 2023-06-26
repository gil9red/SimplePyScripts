#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import sys
import subprocess
import traceback

from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QVBoxLayout, QMessageBox


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.cmd_command = "start cmd.exe @cmd /k ipconfig"

        button_run_subprocess = QPushButton("Run subprocess")
        button_run_subprocess.clicked.connect(self.btn_clicked_subprocess)

        button_os_system = QPushButton("Run os.system")
        button_os_system.clicked.connect(self.btn_clicked_subprocess)

        layout = QVBoxLayout()
        layout.addWidget(button_run_subprocess)
        layout.addWidget(button_os_system)

        self.setLayout(layout)

    def btn_clicked_subprocess(self):
        subprocess.run(self.cmd_command.split(), shell=True)

    def btn_clicked_os_system(self):
        os.system(self.cmd_command)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())
