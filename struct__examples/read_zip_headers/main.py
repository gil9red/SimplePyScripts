#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://pep8.ru/doc/tutorial-3.1/11.html


import struct


with open('myfile.zip', 'rb') as f:
    data = f.read()
    start = 0

    # Показать первые три заголовка
    for _ in range(3):
        start += 14
        fields = struct.unpack('<IIIHH', data[start:start + 16])
        crc32, comp_size, uncomp_size, filenamesize, extra_size = fields

        start += 16
        filename = data[start:start + filenamesize]
        start += filenamesize
        extra = data[start:start + extra_size]

        print('filename: {}, crc32: {}, comp_size: {}, uncomp_size: {}'.format(
            filename, hex(crc32), comp_size, uncomp_size)
        )

        # Пропустить до следующего заголовка
        start += extra_size + comp_size
