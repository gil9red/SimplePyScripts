#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import pandas as pd


def generate_test_data():
    records = [
        (1, "Vasya", 16),
        (2, "Vasya2", 18),
        (3, "Vasya3", 34),
        (4, "Vasya4", 10),
        (5, "Vasya5", 19),
    ]
    return pd.DataFrame(data=records, columns=["ID", "NAME", "AGE"])


if __name__ == "__main__":
    from PyQt5.QtWidgets import *

    # Подготовка данных
    df = generate_test_data()
    headers = df.columns.values.tolist()

    # Отображение данных на виджете
    app = QApplication([])

    table = QTableWidget()
    table.setColumnCount(len(headers))
    table.setHorizontalHeaderLabels(headers)

    for i, row in df.iterrows():
        # Добавление строки
        table.setRowCount(table.rowCount() + 1)

        for j in range(table.columnCount()):
            table.setItem(i, j, QTableWidgetItem(str(row[j])))

    table.show()

    app.exec()
