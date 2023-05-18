#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3.6/library/glob.html#module-glob


import glob
import os


items = glob.glob("../**/*_re.py", recursive=True)
print(items)
print(list(map(os.path.abspath, items)))
print()

# Для папки
items = glob.glob("../**/*_examples/*.py", recursive=True)
print(items)
print(list(map(os.path.abspath, items)))
