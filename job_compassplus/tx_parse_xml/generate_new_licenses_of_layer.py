#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


ITEMS = [
    'W000', 'W001', 'W002', 'W003', 'W004', 'W005', 'W006', 'W007', 'W008', 'W009', 'W010',
    'W011', 'W012', 'W014', 'W015', 'W016', 'W017', 'W018', 'W019', 'W021', 'W022', 'W023',
    'W024', 'W025', 'W026', 'W027', 'W028', 'W029', 'W032', 'W033', 'W034', 'W035', 'W036',
    'W037'
]

text = ''

for name in ITEMS:
    text += f"""\
          <License Name="{name}">
            <RequiredModules/>
          </License>
"""

print(text)
