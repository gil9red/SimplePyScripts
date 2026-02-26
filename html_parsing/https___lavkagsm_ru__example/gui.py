#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.Qt import *

from main import get_html_by_url__from_cache, get_parsed_items
from bs4 import BeautifulSoup


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        headers = ["NAME", "PRICE", "ARTICLE", "URL", "PHOTO_URL"]

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_widget.setSelectionMode(QTableWidget.SingleSelection)
        self.table_widget.itemDoubleClicked.connect(self._on_item_double_click)

        self.setCentralWidget(self.table_widget)

    def fill(self) -> None:
        url = "https://lavkagsm.ru/catalog/mikroskhemy/?view=blocks&page_count=48&sort=name&by=asc"
        html_content = get_html_by_url__from_cache(url)
        root = BeautifulSoup(html_content, "html.parser")

        for item_data in get_parsed_items(url, root):
            row = self.table_widget.rowCount()
            self.table_widget.setRowCount(row + 1)

            self.table_widget.setItem(row, 0, QTableWidgetItem(item_data["name"]))
            self.table_widget.setItem(row, 1, QTableWidgetItem(item_data["price"]))
            self.table_widget.setItem(row, 2, QTableWidgetItem(item_data["art"]))
            self.table_widget.setItem(row, 3, QTableWidgetItem(item_data["url"]))
            self.table_widget.setItem(row, 4, QTableWidgetItem(item_data["photo_url"]))

        self.table_widget.resizeColumnToContents(0)
        self.table_widget.resizeColumnToContents(1)

    def _on_item_double_click(self, item) -> None:
        row = item.row()

        item_url = self.table_widget.item(row, 3)
        url = item_url.text()

        QDesktopServices.openUrl(QUrl(url))


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()
    mw.resize(1500, 800)
    mw.fill()

    app.exec()
