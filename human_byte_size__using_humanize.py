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
    "total: {:>8} ({} bytes)".format(
        humanize.naturalsize(usage.total, binary=True), usage.total
    )
)
print(
    "used:  {:>8} ({} bytes)".format(
        humanize.naturalsize(usage.used, binary=True), usage.used
    )
)
print(
    "free:  {:>8} ({} bytes)".format(
        humanize.naturalsize(usage.free, binary=True), usage.free
    )
)
