#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.stackoverflow.com/a/971228/201445


from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage


class WebEnginePage(QWebEnginePage):
    def createWindow(self, _type):
        page = WebEnginePage(self)
        page.urlChanged.connect(self.on_url_changed)
        return page

    def on_url_changed(self, url: QUrl):
        page = self.sender()
        self.setUrl(url)
        page.deleteLater()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.browser = QWebEngineView()
        self.browser.setPage(WebEnginePage(self.browser))
        self.browser.load(
            QUrl("https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_a_target")
        )

        self.setCentralWidget(self.browser)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
