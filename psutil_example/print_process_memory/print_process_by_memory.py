#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from collections import defaultdict

# pip install psutil
import psutil


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/9007628099adb5964fdbf827f14cc872ba35f8ad/human_byte_size.py
def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)

        num /= 1024.0

    return "%3.1f %s" % (num, 'TB')


column_width = defaultdict(int)
process = []

for p in psutil.process_iter():
    memory = p.memory_info().rss
    cols = p.name(), str(memory) + ' bytes', sizeof_fmt(memory)
    process.append(cols)

    for i, x in enumerate(cols):
        column_width[i] = max(column_width[i], len(x))

# Sort by memory size
process.sort(key=lambda x: int(x[1].split(' ')[0]), reverse=True)

for p in process:
    row = [x.rjust(column_width[i]) for i, x in enumerate(p)]
    print(' | '.join(row))
