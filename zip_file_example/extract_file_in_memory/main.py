#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import zipfile

from pathlib import Path

# pip install humanize
from humanize import naturalsize as sizeof_fmt


FILE_NAME = Path("Doc_df7c89c378c04e8daf69257ea95d9a2e.zip")

print("Zip size:", sizeof_fmt(len(FILE_NAME.read_bytes())))


with zipfile.ZipFile("Doc_df7c89c378c04e8daf69257ea95d9a2e.zip") as f:
    data_file = f.read("Doc_df7c89c378c04e8daf69257ea95d9a2e.html")
    size = sizeof_fmt(len(data_file))
    print(f"File size: {size}")
    print(f"data_file[:100]: {data_file[:100]}")
