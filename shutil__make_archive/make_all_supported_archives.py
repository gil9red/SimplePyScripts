#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3/library/shutil.html#archiving-operations


import os
import shutil


DIR_NAME = "archive"
if not os.path.exists(DIR_NAME):
    os.mkdir(DIR_NAME)


# Make archives
for name, _ in shutil.get_archive_formats():
    file_name = shutil.make_archive(
        base_name=DIR_NAME + "/input.txt",
        format=name,
        base_dir="input_data/input.txt",
    )
    print(file_name)
