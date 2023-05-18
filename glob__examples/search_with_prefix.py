#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3.6/library/glob.html#module-glob


import glob
import os


items = glob.glob("../**/reader_*.py", recursive=True)
print(items)
print(list(map(os.path.abspath, items)))
print()

items = glob.glob("../**/opencv_*/*.py", recursive=True)
print(items)
print(list(map(os.path.abspath, items)))
