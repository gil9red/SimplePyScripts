#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: http://openpyxl.readthedocs.io/en/stable/usage.html#fold-columns-outline


import openpyxl


wb = openpyxl.Workbook()

ws = wb.active
ws.column_dimensions.group('B', 'D', hidden=True)

wb.save('excel.xlsx')
