#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from collections import defaultdict

# pip install psutil
import psutil


column_width = defaultdict(int)
process = []

for p in psutil.process_iter():
    cols = p.name(), str(p.memory_info().rss) + ' bytes'
    process.append(cols)

    for i, x in enumerate(cols):
        column_width[i] = max(column_width[i], len(x))

# Sort by memory size
for p in sorted(process, key=lambda x: int(x[1].split(' ')[0]), reverse=True):
    row = [x.rjust(column_width[i]) for i, x in enumerate(p)]
    print(' | '.join(row))
