#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as DT

# pip install psutil
import psutil


for proc in psutil.process_iter():
    if not proc.name().startswith("python"):
        continue

    secs = proc.create_time()
    started = DT.datetime.fromtimestamp(secs)
    if (DT.datetime.now() - started) >= DT.timedelta(hours=1):
        print(proc)
