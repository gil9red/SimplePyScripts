#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


# pip install psutil

import psutil

print('Disk partitions:')
for disk in psutil.disk_partitions():
    print('  {}'.format(disk))

print()
print('Disk usage:')
for disk in psutil.disk_partitions():
    info = psutil.disk_usage(disk.device)
    print('  {} {}'.format(disk.device, info))
    print('    {} free of {}'.format(sizeof_fmt(info.free), sizeof_fmt(info.total)))
    print()

print()
print('Disk io (input/output) total sum counters:')
print('  {}'.format(psutil.disk_io_counters()))

print()
print('Physical drive io (input/output) counters:')
for drive, info in psutil.disk_io_counters(True).items():
    print('  {}: {}'.format(drive, info))
