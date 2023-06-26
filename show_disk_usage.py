#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import shutil
from human_byte_size import sizeof_fmt


usage = shutil.disk_usage("C://")

print(f"{sizeof_fmt(usage.free)} free of {sizeof_fmt(usage.total)}")
print()
print(f"total: {sizeof_fmt(usage.total):>8} ({usage.total} bytes)")
print(f"used:  {sizeof_fmt(usage.used):>8} ({usage.used} bytes)")
print(f"free:  {sizeof_fmt(usage.free):>8} ({usage.free} bytes)")
