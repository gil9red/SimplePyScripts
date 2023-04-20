#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

# pip install psutil
import psutil


while True:
    for process in psutil.process_iter():
        if process.name() == "calc.exe":
            process.kill()

    # Wait 5 secs
    time.sleep(5)
