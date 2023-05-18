#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3.6/library/glob.html#module-glob


import glob
import os


pattern_template = "../**/*.{}"
patterns = [pattern_template.format(fmt) for fmt in ["jpg", "jpeg", "png", "gif"]]
items = []

for pattern in patterns:
    items += glob.glob(pattern, recursive=True)

items.sort()

print(items)
print(list(map(os.path.abspath, items)))
