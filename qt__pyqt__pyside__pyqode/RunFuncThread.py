#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtCore import QThread, pyqtSignal


class RunFuncThread(QThread):
    run_finished = pyqtSignal(object)

    def __init__(self, func) -> None:
        super().__init__()

        self.func = func

    def run(self) -> None:
        self.run_finished.emit(self.func())


if __name__ == "__main__":
    from PyQt5.QtCore import QCoreApplication

    app = QCoreApplication([])

    thread = RunFuncThread(func=lambda: 2 + 2 * 2)
    thread.run_finished.connect(print)
    thread.finished.connect(app.exit)  # Без app.exec() слоты не сработают
    thread.start()

    app.exec()
