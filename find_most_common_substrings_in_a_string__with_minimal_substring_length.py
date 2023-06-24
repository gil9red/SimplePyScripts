#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from collections import defaultdict


text = "ACGTTGCATGTCGCATGATGCATGAGAGCT"
min_len = 4

accumulator = defaultdict(int)

for length in range(1, len(text) + 1):
    for start in range(len(text) - length):
        sub_text = text[start : start + length]
        accumulator[sub_text] += 1

print(accumulator)

max_items = defaultdict(list)

for k, v in accumulator.items():
    if len(k) >= min_len:
        max_items[v].append(k)

print(max_items)

# Находим ключ с максимальным значением
max_key = max(max_items)
print(max_key, max_items[max_key])  # 3 ['GCAT', 'CATG', 'GCATG']
