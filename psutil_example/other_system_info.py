#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install psutil
import psutil


print("Users:", psutil.users())
print()

boot_time = psutil.boot_time()
print("System boot time (timestamp):", boot_time)

from datetime import datetime
print("System boot time:", datetime.fromtimestamp(boot_time))
