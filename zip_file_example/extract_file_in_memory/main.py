#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


import zipfile
with zipfile.ZipFile('Doc_df7c89c378c04e8daf69257ea95d9a2e.zip') as f:
    data_file = f.read('Doc_df7c89c378c04e8daf69257ea95d9a2e.html')
    size = sizeof_fmt(len(data_file))
    print('Total: {}'.format(size))
    print('data_file[:100]: {}'.format(data_file[:100]))
