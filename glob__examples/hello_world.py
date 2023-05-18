#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3.6/library/glob.html#module-glob


import glob


items = glob.glob("*.py")
print(items)

items = list(glob.iglob("*.py"))
print(items)

print()

for file_name in glob.iglob("*.py"):
    print(file_name)
