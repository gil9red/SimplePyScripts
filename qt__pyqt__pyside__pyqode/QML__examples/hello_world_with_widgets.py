#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from pathlib import Path
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtQuick import QQuickView, QQuickItem
from PyQt5.QtCore import QUrl


QML_FILE = Path(__file__).parent.resolve() / "hello_text.qml"
URL_QML_FILE = QUrl.fromLocalFile(str(QML_FILE))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Hello World! (QML + Qt)')

        self.view = QQuickView()
        self.view.setSource(URL_QML_FILE)

        pb_click = QPushButton('Click me!')
        pb_click.clicked.connect(self._on_clicked)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(QWidget.createWindowContainer(self.view))
        main_layout.addWidget(pb_click)

    def _on_clicked(self):
        qml_hello_text = self.view.rootObject().findChild(QQuickItem, "helloText")
        qml_hello_text.setProperty('text', f'Now: {datetime.now().time():%H:%M:%S}')


if __name__ == '__main__':
    app = QApplication([])

    view = QQuickView()
    view.setTitle('Hello World! (single)')
    view.setSource(URL_QML_FILE)
    view.show()

    main_window = MainWindow()
    main_window.resize(500, 500)
    main_window.show()

    app.exec()
