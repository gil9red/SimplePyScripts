#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import openpyxl


wb = openpyxl.load_workbook('excel.xlsx')
print(wb.get_sheet_names())  # ['Sheet', 'auto', 'Students', 'Students1']

for name in wb.get_sheet_names():
    ws = wb.get_sheet_by_name(name)
    print(name, ws)
