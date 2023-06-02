#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime

# pip install psutil
import psutil


print("Users:", psutil.users())
print()

boot_time = psutil.boot_time()
print("System boot time (timestamp):", boot_time)

print("System boot time:", datetime.fromtimestamp(boot_time))
