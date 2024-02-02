#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

from datetime import datetime, date
from pathlib import Path

from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt


DIR = Path(__file__).parent.resolve()
FILE_NAME_LOGS = DIR / "logs.txt"


def get_date_by_hours(text: str) -> dict[date, list[bool]]:
    items = re.findall(r"\[(.+?),\d+]", text)
    dates = [
        datetime.strptime(item, "%Y-%m-%d %H:%M:%S")
        for item in items
    ]
    dates = sorted(set(dates))

    date_by_hours: dict[date, list[bool]] = dict()
    for d in dates:
        if d.date() not in date_by_hours:
            date_by_hours[d.date()] = [False for _ in range(24)]

        date_by_hours[d.date()][d.hour] = True

    return date_by_hours


if __name__ == "__main__":
    app = QApplication([])

    table_widget = QTableWidget()
    table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    table_widget.show()

    text = FILE_NAME_LOGS.read_text("utf-8")
    date_by_hours = get_date_by_hours(text)

    table_widget.setColumnCount(24)
    for i in range(table_widget.columnCount()):
        table_widget.setHorizontalHeaderItem(i, QTableWidgetItem(str(i)))

    for date_obj, hours in date_by_hours.items():
        row = table_widget.rowCount()
        table_widget.setRowCount(row + 1)

        table_widget.setVerticalHeaderItem(row, QTableWidgetItem(str(date_obj)))

        item = QTableWidgetItem(str(date_obj))

        for col, hour_flag in enumerate(hours):
            item = QTableWidgetItem()

            if hour_flag:
                item.setBackground(Qt.GlobalColor.red)
                item.setForeground(Qt.GlobalColor.white)
            else:
                item.setBackground(Qt.GlobalColor.green)

            table_widget.setItem(row, col, item)

    table_widget.resizeColumnsToContents()

    app.exec()
