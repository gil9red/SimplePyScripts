#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView


app = QApplication([])


with open("js/jquery-3.1.1.min.js") as f:
    jquery_text = f.read()
    jquery_text += "\nvar qt = { 'jQuery': jQuery.noConflict(true) };"


view = QWebEngineView()


def _on_load_finished(ok: bool) -> None:
    view.page().runJavaScript(jquery_text)

    # Test jQuery
    view.page().runJavaScript("qt.jQuery('a').css('background-color', 'yellow');")


view.loadFinished.connect(_on_load_finished)

view.load(QUrl("https://store.steampowered.com/"))
view.show()


app.exec()
