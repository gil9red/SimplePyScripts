#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import pathlib


# Print current folders and files
for file_name in pathlib.Path().glob("*"):
    # print abs path
    print(file_name.resolve())

print()

# Print current folders and files with filter
for file_name in pathlib.Path().glob("get_*"):
    # print abs path
    print(file_name.resolve())

print()

# for file_name in pathlib.Path('../').rglob('*'):
# OR:
for file_name in pathlib.Path("../").glob("**/*"):
    # print abs path
    print(file_name.resolve())
