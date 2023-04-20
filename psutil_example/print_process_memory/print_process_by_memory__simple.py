#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install psutil
import psutil


for p in psutil.process_iter():
    print(p.name(), p.memory_info().rss)
