#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install psutil
import psutil


for p in psutil.process_iter():
    name = p.name()
    if name.lower() != "firefox.exe":
        continue

    print(name, p.memory_info().rss)
