#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://pep8.ru/doc/tutorial-3.1/11.html


import struct


with open('myfile.zip', 'rb') as f:
    rows = []
    headers = ('file_name', 'crc32', 'comp_size', 'uncomp_size')

    data = f.read()
    start = 0

    # Показать первые три заголовка
    for _ in range(3):
        start += 14
        fields = struct.unpack('<IIIHH', data[start:start + 16])
        crc32, comp_size, uncomp_size, file_name_size, extra_size = fields

        start += 16
        file_name = data[start:start + file_name_size]
        file_name = str(file_name, 'utf-8')
        start += file_name_size

        print(
            f'file_name: {file_name}, crc32: {hex(crc32)}, comp_size: {comp_size}, uncomp_size: {uncomp_size}'
        )
        rows.append((file_name, hex(crc32), comp_size, uncomp_size))

        # Пропустить до следующего заголовка
        start += extra_size + comp_size

    print()

    # RESULT:
    # +-------------+------------+-------------+---------------+
    # | file_name   | crc32      |   comp_size |   uncomp_size |
    # +=============+============+=============+===============+
    # | 1.csv       | 0x7eb0f2b2 |          16 |            16 |
    # +-------------+------------+-------------+---------------+
    # | 2.csv       | 0x5d884c77 |          16 |            16 |
    # +-------------+------------+-------------+---------------+
    # | result.csv  | 0xefede9b1 |           8 |             6 |
    # +-------------+------------+-------------+---------------+

    # pip install tabulate
    from tabulate import tabulate
    print(tabulate(rows, headers, tablefmt="grid"))
