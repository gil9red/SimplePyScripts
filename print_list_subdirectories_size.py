#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)

        num /= 1024.0

    return "%3.1f %s" % (num, 'TB')


import os
from os.path import getsize, join


# Словарь нужен чтобы помнить размер папки. Когда итератор дойдет до родительской папки
# в словаре уже будут размер вложенных папок
dir_sizes = dict()

for root, dirs, files in os.walk('.', topdown=False):
    size = sum(getsize(join(root, f)) for f in files)
    size += sum(dir_sizes[join(root, d)] for d in dirs)
    dir_sizes[root] = size

for path, total_size in sorted(dir_sizes.items(), key=lambda x: x[0]):
    print('{} : {} ({})'.format(path, sizeof_fmt(total_size), total_size))
