#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
from pathlib import Path

# pip install psutil
import psutil

sys.path.append(str(Path(__file__).resolve().parent.parent))
from human_byte_size import sizeof_fmt


print('Disk partitions:')
for disk in psutil.disk_partitions():
    print('  {}'.format(disk))

print()
print('Disk usage:')
for disk in filter(lambda x: 'fixed' in x.opts, psutil.disk_partitions()):
    info = psutil.disk_usage(disk.device)
    print('  {} {}'.format(disk.device, info))
    print('    {} free of {}'.format(sizeof_fmt(info.free), sizeof_fmt(info.total)))
    print()

print()
print('Disk io (input/output) total sum counters:')
print('  {}'.format(psutil.disk_io_counters()))


physical_drive_by_info = list(psutil.disk_io_counters(True).items())

print()
print('Physical drive io (input/output) counters ({}):'.format(len(physical_drive_by_info)))
#
# for drive, info in physical_drive_by_info:
#     print('  {}: {}'.format(drive, info))
# #
# # OR:
# #
headers = ('drive',) + physical_drive_by_info[0][1]._fields
headers = [header.upper() for header in headers]

rows = [(drive,) + tuple(info) for drive, info in physical_drive_by_info]

# pip install tabulate
from tabulate import tabulate
print(tabulate(rows, headers=headers, tablefmt="grid"))
print()
print()
