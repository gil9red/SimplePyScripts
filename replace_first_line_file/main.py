#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import shutil


FILE_NAME = "file.txt"

# Create file
with open(FILE_NAME, "w", encoding="utf-8") as f:
    f.write("1\n2\n3\n4\n5")

# Replace first line
from_file = open(FILE_NAME, encoding="utf-8")
line = from_file.readline()
line = "NEW FIRST LINE\n"

to_file = open(FILE_NAME, mode="w", encoding="utf-8")
to_file.write(line)
shutil.copyfileobj(from_file, to_file)
