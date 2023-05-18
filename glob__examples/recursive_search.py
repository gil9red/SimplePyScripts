#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3.6/library/glob.html#module-glob


import glob
import os


items = glob.glob("../*")
print(items)
print(list(map(os.path.abspath, items)))
print()

items = glob.glob("../*.md")
print(items)
print(list(map(os.path.abspath, items)))
print()

items = glob.glob("../**/*.md", recursive=True)
print(items)
print(list(map(os.path.abspath, items)))
print()

items = glob.glob("../**/*.txt", recursive=True)
print(items)
print(list(map(os.path.abspath, items)))
print()

items = glob.glob("../**/*.png", recursive=True)
print(items)
print(list(map(os.path.abspath, items)))
print()
