#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QProgressBar


class FlatProgressBar(QProgressBar):
    def __init__(self, *args):
        super().__init__(*args)

        self.setTextVisible(False)
        self.setStyleSheet(
            """
            QProgressBar {
                background-color: transparent;
                border: 0px solid grey;
                border-radius: 5px;
                max-height: 3px;
                margin-top: 5px;
                margin-bottom: 2px;
            }
            QProgressBar::chunk {
                background-color: gray;
            }
            """
        )

    def setValue(self, value: int):
        super().setValue(value)

        self.setToolTip(
            f"{self.value()} / {self.maximum()} ({self.value() / self.maximum():.1%})"
        )
