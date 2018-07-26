#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


text = 'ACGTTGCATGTCGCATGATGCATGAGAGCT'
max_key_length = 4

from collections import defaultdict
accumulator = defaultdict(int)

for length in range(1, len(text) + 1):
    for start in range(len(text) - length):
        sub_text = text[start: start + length]
        accumulator[sub_text] += 1

print(accumulator)  # {'A': 7, 'C': 6, 'G': 9, 'T': 7,

max_items = defaultdict(list)

for k, v in accumulator.items():
    if len(k) != max_key_length:
        continue

    max_items[v].append(k)

print(max_items)  # ... , 2: ['TGCA', 'ATGA'], 3: ['GCAT', 'CATG']})

# Находим ключ с максимальным значением
max_key = max(max_items)
print(max_items[max_key])  # ['GCAT', 'CATG']
