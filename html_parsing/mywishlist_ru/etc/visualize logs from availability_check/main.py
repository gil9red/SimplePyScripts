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
    date_by_hours: dict[date, list[bool | None]] = dict()

    for line in text.splitlines():
        m = re.search(r"\[(.+?),\d+]", line)
        if not m:
            continue

        dt = datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")

        date_obj = dt.date()
        if date_obj not in date_by_hours:
            date_by_hours[date_obj] = [None for _ in range(24)]

        date_by_hours[date_obj][dt.hour] = "Сайт доступен" in line

    # Нужно заполнить промежутки между часами - например,
    # сайт был доступен с 13 до 17, но в логах будут только 13 и 17
    last_available = None
    for hours in date_by_hours.values():
        for i, flag in enumerate(hours):
            if flag is not None:
                last_available = flag
                continue

            if last_available is None:
                continue

            if flag is None:
                hours[i] = last_available

    return date_by_hours


if __name__ == "__main__":
    app = QApplication([])

    table_widget = QTableWidget()
    table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    table_widget.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

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

            if hour_flag is not None:
                if hour_flag:
                    item.setBackground(Qt.GlobalColor.green)
                else:
                    item.setBackground(Qt.GlobalColor.red)
                    item.setForeground(Qt.GlobalColor.white)

            table_widget.setItem(row, col, item)

    table_widget.resizeColumnsToContents()

    app.exec()
