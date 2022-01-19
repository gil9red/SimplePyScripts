#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import Any

# pip install PyQt5
from PyQt5.QtWidgets import QApplication

# pip install PyQtWebEngine
from PyQt5.QtWebEngineWidgets import QWebEnginePage


app = QApplication([])


def run_js(code: str) -> Any:
    result: Any = None
    callback_finished = False

    def _callback(v):
        nonlocal result, callback_finished
        result = v
        callback_finished = True

    page = QWebEnginePage()
    page.runJavaScript(code, _callback)

    while not callback_finished:
        QApplication.processEvents()

    return result


if __name__ == '__main__':
    print(run_js("2+2"))
    print(run_js("let f = a => a*2; f(10)"))
    print(run_js("""
        let f = a => a*2;
        f(10);
    """))
    print(run_js("""
        function f(a) {
            return a * 2;
        }
        f(10);
    """))
