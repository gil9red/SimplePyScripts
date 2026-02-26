#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
from PyQt5.Qt import QMainWindow, QLabel, QFont, QApplication, Qt, QThread


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Courier", 25))

        def loop() -> None:
            i = 0

            while True:
                self.label.setText(str(i))

                i += 1
                time.sleep(1)

        class Thread(QThread):
            def run(self) -> None:
                loop()

        self.thread = Thread()
        self.thread.start()

        self.setCentralWidget(self.label)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
