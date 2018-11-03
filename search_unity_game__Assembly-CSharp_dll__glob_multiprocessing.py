#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import typing
import glob
import os
from multiprocessing import Pool


def get_filename_list(pattern: str) -> typing.List[str]:
    pattern = os.path.normpath(pattern)
    return glob.glob(pattern, recursive=True)


if __name__ == '__main__':
    drivers = ['C', 'D', 'E']

    with Pool() as p:
        pattern_list = ['{}:/**/*Data/Managed/Assembly-CSharp.dll'.format(x) for x in drivers]
        result = p.map(get_filename_list, pattern_list)

        file_names = []

        for sub in result:
            file_names += sub

        file_names.sort()

        print(len(file_names))
        for file_name in file_names:
            print(file_name)
