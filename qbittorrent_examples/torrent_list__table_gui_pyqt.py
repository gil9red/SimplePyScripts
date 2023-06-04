#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/qbittorrent/qbittorrent/wiki/WebUI-API-Documentation#get-torrent-list


from PyQt5.Qt import *

from common import get_client


class TorrentInfoWidget(QTableWidget):
    def __init__(self):
        super().__init__()

        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSelectionMode(QTableWidget.SingleSelection)

        headers = ["KEY", "VALUE"]
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)

        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def fill(self, torrent_details: dict):
        while self.rowCount():
            self.removeRow(0)

        for k, v in torrent_details.items():
            row = self.rowCount()
            self.setRowCount(row + 1)

            self.setItem(row, 0, QTableWidgetItem(str(k)))
            self.setItem(row, 1, QTableWidgetItem(str(v)))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table_torrent = QTableWidget()
        self.table_torrent.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_torrent.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_torrent.setSelectionMode(QTableWidget.SingleSelection)
        self.table_torrent.itemSelectionChanged.connect(self.fill_torrent_info)

        self.torrent_info_widget = TorrentInfoWidget()

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.table_torrent)
        splitter.addWidget(self.torrent_info_widget)

        self.setCentralWidget(splitter)

    def fill_table(self):
        qb = get_client()
        torrents = qb.torrents()
        if not torrents:
            return

        self.table_torrent.clear()

        headers = torrents[0].keys()
        self.table_torrent.setColumnCount(len(headers))
        self.table_torrent.setHorizontalHeaderLabels(headers)

        self.table_torrent.setRowCount(len(torrents))

        for row, torrent in enumerate(torrents):
            for column, key in enumerate(headers):
                value = str(torrent[key])

                item = QTableWidgetItem(value)
                item.setData(Qt.UserRole, torrent)

                self.table_torrent.setItem(row, column, item)

    def fill_torrent_info(self):
        items = self.table_torrent.selectedItems()
        if not items:
            return

        torrent = items[0].data(Qt.UserRole)

        qb = get_client()
        torrent_details = qb.get_torrent(torrent["hash"])

        self.torrent_info_widget.fill(torrent_details)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.resize(900, 600)
    mw.show()
    mw.fill_table()

    app.exec()
