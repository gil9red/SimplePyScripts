#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView


LOGIN = "<LOGIN>"
PASSWORD = "<PASSWORD>"


file_name = "../QWebEngine__append_custom_javascript__jQuery/js/jquery-3.1.1.min.js"
with open(file_name) as f:
    jquery_text = f.read()
    jquery_text += "\nvar qt = { 'jQuery': jQuery.noConflict(true) };"


app = QApplication([])

view = QWebEngineView()
view.load(QUrl("https://github.com/login"))


def _on_load_finished(ok: bool):
    page = view.page()

    url = page.url().toString()
    print(url)

    if not url.endswith("login"):
        return

    page.runJavaScript(jquery_text)

    page.runJavaScript(
        f"""
    qt.jQuery('#login_field').val('{LOGIN}');
    qt.jQuery('#password').val('{PASSWORD}');
    
    qt.jQuery('input[name="commit"]').click();
    """
    )

    print()


view.loadProgress.connect(
    lambda value: view.setWindowTitle("{} ({}%)".format(view.url().toString(), value))
)
view.loadFinished.connect(_on_load_finished)

mw = QMainWindow()
mw.setCentralWidget(view)
mw.resize(500, 500)
mw.show()

app.exec()
