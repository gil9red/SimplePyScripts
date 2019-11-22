#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from os import walk
from os.path import join, getsize


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)

        num /= 1024.0

    return "%3.1f %s" % (num, 'TB')


for root_dir in [r'C:\DEV__TX', r'C:\DEV__OPTT', r'C:\DEV__RADIX']:
    print('Check:', root_dir)

    for root, dirs, files in walk(root_dir):
        for f in files:
            file_name = join(root, f)
            file_size = getsize(file_name)
            if '.hprof' in f or file_size >= 1_000_000_000:  # 1 GB
                print(file_name, file_size, sizeof_fmt(file_size))
