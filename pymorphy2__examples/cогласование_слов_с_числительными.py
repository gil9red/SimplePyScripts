#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install pymorphy2
import pymorphy2

# pip install tabulate
from tabulate import tabulate


morph = pymorphy2.MorphAnalyzer()


words = [
    'программист',
    'ёлка',
    'фрукт',
    'игр',
    'барсук'
]
parsed_words = [morph.parse(word)[0] for word in words]

rows = []
for i in range(5 + 1):
    row = []
    for parsed_word in parsed_words:
        word = parsed_word.make_agree_with_number(i).word
        row.append(f'{i} {word}')
    rows.append(row)

print(tabulate(rows, headers=words, tablefmt="orgtbl"))
"""
| программист     | ёлка   | фрукт     | игр    | барсук     |
|-----------------+--------+-----------+--------+------------|
| 0 программистов | 0 ёлок | 0 фруктов | 0 игр  | 0 барсуков |
| 1 программист   | 1 ёлка | 1 фрукт   | 1 игры | 1 барсук   |
| 2 программиста  | 2 ёлки | 2 фрукта  | 2 игр  | 2 барсука  |
| 3 программиста  | 3 ёлки | 3 фрукта  | 3 игр  | 3 барсука  |
| 4 программиста  | 4 ёлки | 4 фрукта  | 4 игр  | 4 барсука  |
| 5 программистов | 5 ёлок | 5 фруктов | 5 игр  | 5 барсуков |
"""
