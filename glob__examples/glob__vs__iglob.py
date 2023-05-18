#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3.6/library/glob.html#module-glob
# SOURCE: https://docs.python.org/3.6/library/glob.html#glob.iglob


import glob
import os


pattern = "../**/*.py"

# First `glob` will collect all the results, and then return the list
for file_name in glob.glob(pattern, recursive=True):
    print(os.path.abspath(file_name))

print("\n" + "-" * 50 + "\n")

# iglob returns an iterator that will return the next pattern found by the path at each iteration
for file_name in glob.iglob(pattern, recursive=True):
    print(os.path.abspath(file_name))
