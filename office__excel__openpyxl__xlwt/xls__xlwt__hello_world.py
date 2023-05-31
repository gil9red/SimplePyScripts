#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install xlwt
import xlwt


columns = ["Name", "Age", "Course"]
rows = [
    ["Vasya", "16", 1],
    ["Anya", "17", 2],
    ["Inna", "16", 1],
]


wb = xlwt.Workbook()
ws = wb.add_sheet("Students")

for i, column in enumerate(columns):
    ws.write(0, i, column)

for i, row in enumerate(rows, 1):
    for j, data in enumerate(row):
        ws.write(i, j, data)

wb.save("excel.xls")
