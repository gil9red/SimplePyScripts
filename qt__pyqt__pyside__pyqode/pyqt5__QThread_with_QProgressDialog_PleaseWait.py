#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
from PyQt5.Qt import *


class RunFuncThread(QThread):
    run_finished = pyqtSignal(object)

    def __init__(self, func):
        super().__init__()

        self.func = func

    def run(self):
        self.run_finished.emit(self.func())


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.pb_go = QPushButton("Go")
        self.pb_go.clicked.connect(self.go)

        self.te_log = QPlainTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.pb_go)
        layout.addWidget(self.te_log)

        self.setLayout(layout)

    def _on_run_finished(self, value):
        self.te_log.setPlainText(str(value))

    def go(self):
        progress_dialog = QProgressDialog(self)

        def foo():
            items = []

            for i in range(10):
                items.append(i)
                i -= 1

                time.sleep(0.5)

            return items

        thread = RunFuncThread(func=foo)
        thread.run_finished.connect(self._on_run_finished)
        thread.run_finished.connect(progress_dialog.close)
        thread.start()

        progress_dialog.setWindowTitle("Please wait...")
        progress_dialog.setLabelText(progress_dialog.windowTitle())
        progress_dialog.setRange(0, 0)
        progress_dialog.exec()


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
