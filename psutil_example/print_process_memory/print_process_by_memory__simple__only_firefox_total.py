#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install psutil
import psutil


total = 0

for p in psutil.process_iter():
    name = p.name()
    if name.lower() != "firefox.exe":
        continue

    memory = p.memory_info().rss
    total += memory

    print(name, memory)

print(f"""
Total: {total} bytes
       {total // 1024} KB
       {total // 1024 // 1024} MB
       {total // 1024 // 1024 // 1024} GB
""")
