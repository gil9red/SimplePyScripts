#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install psutil
import psutil

print("CPU info:", psutil.cpu_times())

print()
for _ in range(3):
    info = psutil.cpu_percent(interval=1)
    print("CPU percent (interval=1, percpu=False):", info)

print()
for _ in range(3):
    info = psutil.cpu_percent(interval=1, percpu=True)
    print("CPU percent (interval=1, percpu=True):", info)

print()
for _ in range(3):
    info = psutil.cpu_times_percent(interval=1, percpu=False)
    print("CPU times percent (interval=1, percpu=False):", info)

print()
print("Logical CPUs:", psutil.cpu_count())
print("Physical CPUs:", psutil.cpu_count(logical=False))

print()
print("CPU stats:", psutil.cpu_stats())
print("CPU freq:", psutil.cpu_freq())
