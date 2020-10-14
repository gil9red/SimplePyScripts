#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import Union


def sizeof_fmt(num: Union[int, float]) -> str:
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%.1f %s" % (num, x)

        num /= 1024.0

    return "%.1f %s" % (num, 'TB')


if __name__ == '__main__':
    print(sizeof_fmt(25000000000))
    print()

    import shutil
    usage = shutil.disk_usage('C://')
    print('total: {:>8} ({} bytes)'.format(sizeof_fmt(usage.total), usage.total))
    print('used:  {:>8} ({} bytes)'.format(sizeof_fmt(usage.used), usage.used))
    print('free:  {:>8} ({} bytes)'.format(sizeof_fmt(usage.free), usage.free))
