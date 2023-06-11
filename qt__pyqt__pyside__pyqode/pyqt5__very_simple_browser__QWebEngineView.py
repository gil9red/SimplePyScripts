#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.Qt import (
    QWebEngineView,
    QApplication,
    QUrl,
    QWidget,
    QLineEdit,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("...")

        self.url_le = QLineEdit("http://qt-project.org/")

        self.go_pb = QPushButton("Go")
        self.go_pb.clicked.connect(self._on_load_url)

        url_layout = QHBoxLayout()
        url_layout.addWidget(self.url_le)
        url_layout.addWidget(self.go_pb)

        self.view = QWebEngineView()
        self.view.urlChanged.connect(self._on_url_changed)
        self.view.titleChanged.connect(self.setWindowTitle)

        main_layout = QVBoxLayout()
        main_layout.addLayout(url_layout)
        main_layout.addWidget(self.view)

        self.setLayout(main_layout)

    def _on_load_url(self):
        self.view.load(QUrl(self.url_le.text()))

    def _on_url_changed(self, url: QUrl):
        self.url_le.setText(url.toString())


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
