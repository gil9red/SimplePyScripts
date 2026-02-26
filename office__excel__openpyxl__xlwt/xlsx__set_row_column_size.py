#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import openpyxl
from openpyxl.worksheet.worksheet import Worksheet


def set_row_column_size(ws: Worksheet) -> None:
    # SOURCE: excel__openpyxl__xlwt\excel\xl\worksheets\sheet1.xml
    # <sheetFormatPr defaultColWidth="1.77734375" defaultRowHeight="6.6" customHeight="1" x14ac:dyDescent="0.3"/>
    ws.sheet_format.defaultColWidth = 1.77734375
    ws.sheet_format.defaultRowHeight = 9.0
    ws.sheet_format.customHeight = 1


wb = openpyxl.Workbook()

# Sheet 2
ws = wb.create_sheet()
set_row_column_size(ws)

wb.save("excel.xlsx")
