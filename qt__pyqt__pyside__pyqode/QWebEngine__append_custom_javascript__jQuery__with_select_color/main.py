#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.view = QWebEngineView()
        self.view.loadFinished.connect(self._on_load_finished)

        file_name = "../QWebEngine__append_custom_javascript__jQuery/js/jquery-3.1.1.min.js"
        with open(file_name) as f:
            self.jquery_text = f.read()
            self.jquery_text += "\nvar qt = { 'jQuery': jQuery.noConflict(true) };"

        tool_bar = self.addToolBar("General")
        action = tool_bar.addAction("Change <a> background-color")
        action.triggered.connect(self._change_background_color)

        self.setCentralWidget(self.view)

    def _on_load_finished(self, ok: bool):
        self.view.page().runJavaScript(self.jquery_text)

    def _change_background_color(self):
        color = QColorDialog.getColor(Qt.yellow)
        if not color.isValid():
            return

        code = f"qt.jQuery('a').css('background-color', '{color.name()}');"
        self.view.page().runJavaScript(code)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.resize(400, 400)
    mw.show()

    mw.view.load(QUrl("https://store.steampowered.com/"))

    app.exec()
