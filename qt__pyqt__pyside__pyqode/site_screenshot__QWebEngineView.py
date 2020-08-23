#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://stackoverflow.com/a/57957098/5909792


import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings


class Screenshot(QWebEngineView):
    def __init__(self, app: QApplication):
        super().__init__()

        self.app = app

    def capture(self, url: str, output_file: str):
        self.output_file = output_file
        self.load(QUrl(url))
        self.loadFinished.connect(self.on_loaded)

        # Create hidden view without scrollbars
        self.setAttribute(Qt.WA_DontShowOnScreen)
        self.page().settings().setAttribute(
            QWebEngineSettings.ShowScrollBars, False
        )

        self.show()

    def on_loaded(self):
        size = self.page().contentsSize().toSize()
        self.resize(size)
        # Wait for resize
        QTimer.singleShot(1000, self.take_screenshot)

    def take_screenshot(self):
        self.grab().save(self.output_file, 'PNG')
        self.app.quit()


app = QApplication(sys.argv)
s = Screenshot(app)
s.capture('https://pypi.org/project/PyQt5/', 'webpage.png')
sys.exit(app.exec_())
