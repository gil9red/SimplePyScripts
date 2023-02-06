#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import openpyxl


# NOTE: from xlsx__hyperlink_cell_to_sheet.py
filename = 'excel.xlsx'

wb = openpyxl.load_workbook(filename=filename)

sheet1 = wb['Sheet']
sheet2 = wb['Лист 2']

sheet1.cell(row=5, column=1).hyperlink = f"#'{sheet2.title}'!B20"
sheet1.cell(row=5, column=1).value = "Go2"

wb.save(filename)
