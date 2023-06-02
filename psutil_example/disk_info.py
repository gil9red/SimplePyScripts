#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install humanize
from humanize import naturalsize as sizeof_fmt

# pip install psutil
import psutil

# pip install tabulate
from tabulate import tabulate


print("Disk partitions:")
for disk in psutil.disk_partitions():
    print(f"  {disk}")

print()
print("Disk usage:")
for disk in filter(lambda x: "fixed" in x.opts, psutil.disk_partitions()):
    info = psutil.disk_usage(disk.device)
    print(f"  {disk.device} {info}")
    print(f"    {sizeof_fmt(info.free)} free of {sizeof_fmt(info.total)}")
    print()

print()
print("Disk io (input/output) total sum counters:")
print(f"  {psutil.disk_io_counters()}")


physical_drive_by_info = list(psutil.disk_io_counters(True).items())

print()
print(f"Physical drive io (input/output) counters ({len(physical_drive_by_info)}):")

headers = ("drive",) + physical_drive_by_info[0][1]._fields
headers = [header.upper() for header in headers]

rows = [(drive,) + tuple(info) for drive, info in physical_drive_by_info]
print(tabulate(rows, headers=headers, tablefmt="grid"))
