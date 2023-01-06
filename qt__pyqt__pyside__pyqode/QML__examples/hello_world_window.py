#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from pathlib import Path


from PyQt5.QtGui import QGuiApplication  # NOTE: For only QML, QGuiApplication is enough
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QUrl


app = QGuiApplication([])

qml_file_window = Path(__file__).parent.resolve() / "hello_text_window.qml"
url_qml_file_window = QUrl.fromLocalFile(str(qml_file_window))

engine = QQmlApplicationEngine(url_qml_file_window)

app.exec()
