#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import shutil

# pip install humanize
import humanize


print(humanize.naturalsize(25000000000, binary=True))  # '23.3 GiB'
print(
    humanize.naturalsize(25000000000, binary=True).replace("i", "")
)  # '23.3 GB',   Strange, misleading
print()

usage = shutil.disk_usage("C://")
print(
    f"total: {humanize.naturalsize(usage.total, binary=True):>8} ({usage.total} bytes)"
)
print(
    f"used:  {humanize.naturalsize(usage.used, binary=True):>8} ({usage.used} bytes)"
)
print(
    f"free:  {humanize.naturalsize(usage.free, binary=True):>8} ({usage.free} bytes)"
)
