#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


import shutil
usage = shutil.disk_usage('C://')

print('{} free of {}'.format(sizeof_fmt(usage.free), sizeof_fmt(usage.total)))
print()
print('total: {:>8} ({} bytes)'.format(sizeof_fmt(usage.total), usage.total))
print('used:  {:>8} ({} bytes)'.format(sizeof_fmt(usage.used), usage.used))
print('free:  {:>8} ({} bytes)'.format(sizeof_fmt(usage.free), usage.free))
