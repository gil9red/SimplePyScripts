#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Плагин удаляет из архива указанные в exclude файлы.
xpi файл -- плагин для FireFox, является zip архивом."""


import os.path
import sys
from zipfile import ZipFile


def do(zip_file_name):
    print('zip_file_name:', zip_file_name)

    exclude = ['README.md', 'run.bat', 'xpi.bat']

    print('Delete files:', exclude)

    # Измененный zip
    out_zip_file_name = '_' + zip_file_name

    try:
        print('open {} and {} zip arhives'.format(zip_file_name, out_zip_file_name))
        zin = ZipFile(zip_file_name, 'r')
        zout = ZipFile(out_zip_file_name, 'w')

        print('start fill {} zip arhive'.format(out_zip_file_name))

        for item in zin.infolist():
            buffer = zin.read(item.filename)
            if os.path.basename(item.filename) not in exclude:
                zout.writestr(item, buffer)

        print('finish fill {} zip arhive'.format(out_zip_file_name))

    finally:
        zout.close()
        zin.close()

        # Удаляем оригинальный
        print('remove original {} zip file'.format(zip_file_name))
        os.remove(zip_file_name)

        # Переименновываем измененный zip в оригинальный
        print('rename {} zip file as original {}'.format(out_zip_file_name, zip_file_name))
        os.rename(out_zip_file_name, zip_file_name)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        zip_file_name = ' '.join(sys.argv[1:])

        # # Оригинальный zip
        # zip_file_name = '@closingduplicatetabs-0.0.2.xpi'

        do(zip_file_name)

    else:
        file_name = os.path.basename(sys.argv[0])
        print('usage: {} [-h] zip_file_name'.format(file_name))
