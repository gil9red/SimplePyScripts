#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtCore import QUrl, QEventLoop
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage


def run_js_code(page: QWebEnginePage, code: str) -> object:
    loop = QEventLoop()

    result_value = {"value": None}

    def _on_callback(result: object):
        result_value["value"] = result

        loop.quit()

    page.runJavaScript(code, _on_callback)

    loop.exec()

    return result_value["value"]


file_name = "../QWebEngine__append_custom_javascript__jQuery/js/jquery-3.1.1.min.js"
with open(file_name) as f:
    jquery_text = f.read()
    jquery_text += "\nvar qt = { 'jQuery': jQuery.noConflict(true) };"


app = QApplication([])

view = QWebEngineView()
view.load(QUrl("https://гибдд.рф/request_main"))


def _on_load_finished(ok: bool):
    page = view.page()
    print(page.url().toString())

    page.runJavaScript(jquery_text)

    result = run_js_code(page, "document.title")
    print("run_java_script:", result)

    # Клик на флажок "С информацией ознакомлен"
    run_js_code(page, """qt.jQuery('input[name="agree"]').click();""")

    # Клик на кнопку "Подать обращение"
    run_js_code(page, """qt.jQuery('button.u-form__sbt').click();""")

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
