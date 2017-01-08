#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def md5sum(filename):
    """
    Функция для получения контрольной суммы файла, используя алгоритм MD5.

    """

    import hashlib
    md5 = hashlib.md5()

    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
            md5.update(chunk)

    return md5.hexdigest()


if __name__ == '__main__':
    file_name = r'C:\Program Files (x86)\Agarest_Generations of War Zero\AgarestZero.exe'
    print(md5sum(file_name))
