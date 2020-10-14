#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import time
from os.path import join

from human_byte_size import sizeof_fmt


def get_files_info(dir_name):
    for root, dirs, files in os.walk(dir_name):
        for file_name in files:
            abs_file_name = join(root, file_name)

            yield abs_file_name, os.stat(abs_file_name)


def get_date_as_string(dt):
    return time.strftime('%H:%M:%S %m.%d.%y', time.gmtime(dt))


if __name__ == '__main__':
    dir_name = r"D:\Program Files (x86)\Microsoft Office"

    # Сортировка по размеру
    files_sorted_by_size = sorted(get_files_info(dir_name), reverse=True, key=lambda x: x[1].st_size)

    # # Без сортировки
    # files_sorted_by_size = get_files_info(dir_name)

    # Сохраняем в HTML файл
    with open('result.html', 'w', encoding='utf-8') as f:
        f.write('''
        <html>
            <head>
                <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
                <style>
                    /* Добавление сетки таблицы */
                    table {
                        border-collapse: collapse; /* Убираем двойные линии между ячейками */
                    }
                    td, th {
                        padding: 3px; /* Поля вокруг содержимого таблицы */
                        border: 1px solid black; /* Параметры рамки */
                    }
                </style>
            </head>
            <body>
                <table>
        ''')

        f.write('<capture>{}</capture>'.format(dir_name))

        f.write('<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format('FILE NAME', 'SIZE', 'LAST MODIFICATION'))

        for file_name, file_stat in files_sorted_by_size:
            f.write('<tr>')

            f.write('<td>{}</td><td>{}</td><td>{}</td>'.format(
                '<a href="file://{f}">{f}</a>'.format(f=file_name),
                sizeof_fmt(file_stat.st_size),
                get_date_as_string(file_stat.st_mtime)
            ))

            f.write('</tr>')

        f.write('''
                </table>
            </body>
        </html>
        ''')
