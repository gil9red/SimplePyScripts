#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Плагин удаляет из архива указанные в exclude файлы.
xpi файл -- плагин для FireFox, является zip архивом."""


import os.path
from zipfile import ZipFile


EXCLUDE = ['README.md', 'run.bat', 'xpi.bat']


import argparse


def create_parser():
    parser = argparse.ArgumentParser(description='Remove unnecessary files from zip.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('zip_file_name', type=str)
    parser.add_argument('--exclude', nargs='*', default=EXCLUDE)
    parser.add_argument('--add_exclude', action='store_true')

    return parser.parse_args()


def do(zip_file_name, exclude):
    print('zip_file_name:', zip_file_name)

    print('Delete files:', EXCLUDE)

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
    args = create_parser()

    exclude = EXCLUDE + args.exclude if args.add_exclude else args.exclude
    do(args.zip_file_name, set(exclude))
