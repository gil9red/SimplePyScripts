#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView
from PyQt5.QtCore import QUrl


app = QGuiApplication([])

qml_file = Path(__file__).parent.resolve() / "hello_text.qml"
url_qml_file = QUrl.fromLocalFile(str(qml_file))

view = QQuickView()
view.setTitle("Hello World!")
view.setSource(url_qml_file)
view.show()

app.exec()
