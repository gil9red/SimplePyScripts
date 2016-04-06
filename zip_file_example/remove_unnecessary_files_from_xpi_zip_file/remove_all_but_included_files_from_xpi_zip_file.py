#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Плагин удаляет из архива все файлы кроме указанных.
xpi файл -- плагин для FireFox, является zip архивом."""


import os.path
import fnmatch
from zipfile import ZipFile


INCLUDE = ['data/*', 'index.js', 'bootstrap.js', 'package.json', 'install.rdf']


import argparse


def create_parser():
    parser = argparse.ArgumentParser(description='Remove all but included files from zip.py.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('zip_file_name', type=str)
    parser.add_argument('--include', nargs='*', default=INCLUDE)
    parser.add_argument('--add_include', action='store_true')

    return parser.parse_args()


def do(zip_file_name, include):
    print('zip_file_name:', zip_file_name)
    print('Include files:', include)

    # Измененный zip
    out_zip_file_name = '_' + zip_file_name

    try:
        print('open {} and {} zip arhives'.format(zip_file_name, out_zip_file_name))
        zin = ZipFile(zip_file_name, 'r')
        zout = ZipFile(out_zip_file_name, 'w')

        print('start fill {} zip arhive'.format(out_zip_file_name))

        for item in zin.infolist():
            buffer = zin.read(item.filename)

            if any((fnmatch.fnmatch(item.filename, pattern) for pattern in include)):
                zout.writestr(item, buffer)
            else:
                print('Delete', item.filename)

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

    include = set(INCLUDE + args.include if args.add_include else args.include)
    do(args.zip_file_name, include)

    # do('@closingduplicatetabs-0.0.2.xpi', INCLUDE)
