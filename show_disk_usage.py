#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import shutil
from human_byte_size import sizeof_fmt


usage = shutil.disk_usage('C://')

print('{} free of {}'.format(sizeof_fmt(usage.free), sizeof_fmt(usage.total)))
print()
print('total: {:>8} ({} bytes)'.format(sizeof_fmt(usage.total), usage.total))
print('used:  {:>8} ({} bytes)'.format(sizeof_fmt(usage.used), usage.used))
print('free:  {:>8} ({} bytes)'.format(sizeof_fmt(usage.free), usage.free))
