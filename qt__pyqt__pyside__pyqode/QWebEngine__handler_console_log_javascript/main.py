#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage


class MyWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(
        self,
        level: "JavaScriptConsoleMessage",
        message: str,
        line_number: int,
        source_id: str,
    ) -> None:
        print(
            f"javascript_console_message: {level}, {message}, {line_number}, {source_id}",
            file=sys.stderr,
        )


app = QApplication([])

page = MyWebEnginePage()
page.load(QUrl("https://ya.ru"))

view = QWebEngineView()
view.setPage(page)


def _on_load_finished(ok: bool) -> None:
    page = view.page()
    print(page.url().toString())

    page.runJavaScript("console.log(document.title)")
    page.runJavaScript("console.log(this)")
    page.runJavaScript('console.log("Hello World!")')
    page.runJavaScript("console.log(2 + 2 * 2)")

    print()


view.loadProgress.connect(
    lambda value: view.setWindowTitle(f"{view.url().toString()} ({value}%)")
)
view.loadFinished.connect(_on_load_finished)

mw = QMainWindow()
mw.setCentralWidget(view)
mw.resize(500, 500)
mw.show()

app.exec()
