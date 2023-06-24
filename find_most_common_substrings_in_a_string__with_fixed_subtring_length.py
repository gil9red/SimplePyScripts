#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from collections import defaultdict, Counter


text = "ACGTTGCATGTCGCATGATGCATGAGAGCT"
key_len = 4

accumulator = Counter(text[i : i + key_len] for i in range(len(text) - key_len + 1))
print(accumulator)  # {'A': 7, 'C': 6, 'G': 9, 'T': 7,

max_items = defaultdict(list)

for k, v in accumulator.items():
    max_items[v].append(k)

print(max_items)  # ... , 2: ['TGCA', 'ATGA'], 3: ['GCAT', 'CATG']})

# Находим ключ с максимальным значением
max_key = max(max_items)
print(max_key, max_items[max_key])  # 3 ['GCAT', 'CATG']
