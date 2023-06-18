#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import glob
import os

from multiprocessing import Pool
from itertools import chain


def get_filename_list(pattern: str) -> list[str]:
    pattern = os.path.normpath(pattern)
    return glob.glob(pattern, recursive=True)


if __name__ == "__main__":
    drivers = ["C", "D", "E"]

    with Pool() as p:
        pattern_list = [x + ":/**/*Data/Managed/Assembly-CSharp.dll" for x in drivers]
        result = p.map(get_filename_list, pattern_list)

        file_names = sorted(chain.from_iterable(result))
        print(len(file_names))

        for file_name in file_names:
            print(file_name)
