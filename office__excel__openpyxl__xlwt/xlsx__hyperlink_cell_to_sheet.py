#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import openpyxl


wb = openpyxl.Workbook()

sheet1 = wb.active

sheet2 = wb.create_sheet(title='Лист 2')

sheet1.cell(row=1, column=1).hyperlink = f"#'{sheet2.title}'!K20"
sheet1.cell(row=1, column=1).value = "Go"

wb.save('excel.xlsx')
