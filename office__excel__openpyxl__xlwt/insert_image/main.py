#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: http://openpyxl.readthedocs.io/en/stable/usage.html#inserting-an-image


import openpyxl
from openpyxl.drawing.image import Image


wb = openpyxl.Workbook()
ws = wb.active

ws['A1'] = 'You should see three logos below'

# Create an image
img = Image('logo.png')

# Add to worksheet and anchor next to cells
ws.add_image(img, 'A2')

wb.save('excel.xlsx')
