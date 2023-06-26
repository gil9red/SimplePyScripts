#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
from datetime import datetime

# pip install psutil
import psutil

# pip install humanize
from humanize import naturalsize as sizeof_fmt


while True:
    for p in psutil.process_iter():
        if p.name() == "TS3W.exe":
            memory_info = p.memory_info()

            fields = memory_info._asdict().items()
            fields = sorted(fields, key=lambda x: x[1], reverse=True)
            print(
                f"{datetime.now():%H:%M:%S}",
                ", ".join(f"{k}: {sizeof_fmt(v)}" for k, v in fields),
            )

    time.sleep(60)
