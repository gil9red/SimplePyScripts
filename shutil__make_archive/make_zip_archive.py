#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3/library/shutil.html#archiving-operations


import os
import shutil


DIR_NAME = "archive"
if not os.path.exists(DIR_NAME):
    os.mkdir(DIR_NAME)


file_name = shutil.make_archive(
    base_name=DIR_NAME + "/input.txt",
    format="zip",
    base_dir="input_data/input.txt",
)
print(file_name)  # archive/input.txt.zip

file_name = shutil.make_archive(
    base_name=DIR_NAME + "/input_dir",
    format="zip",
    base_dir="input_data/input_dir",
)
print(file_name)  # archive/input_dir.zip

file_name = shutil.make_archive(
    base_name=DIR_NAME + "/input_data",
    format="zip",
    base_dir="input_data",
)
print(file_name)  # archive/input_dir.zip
