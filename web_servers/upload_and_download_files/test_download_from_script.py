#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)

        num /= 1024.0

    return "%3.1f %s" % (num, 'TB')


def progress(count, block_size, total_size):
    percent = count * block_size * 100.0 / total_size
    print("Download: %s/%s(%3.1f%%)" % (sizeof_fmt(count * block_size), sizeof_fmt(total_size), percent) + ' ' * 20,
          end='\r')


def create_test_file():
    file_name = 'uploads/bigfile'

    import os
    if os.path.exists(file_name):
        return

    # Создание больших файлов для теста
    with open(file_name, 'wb') as f:
        for i in range(1024 * 1024 * 600):
            f.write(b'0')

if __name__ == '__main__':
    create_test_file()

    from urllib.request import urlretrieve
    urlretrieve('http://127.0.0.1:5000/files/bigfile', "file", reporthook=progress)
