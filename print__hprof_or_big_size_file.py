#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from os import walk
from os.path import join, getsize
from timeit import default_timer
from multiprocessing.dummy import Pool as ThreadPool

from human_byte_size import sizeof_fmt


DIRS = [r'C:\DEV__TX', r'C:\DEV__OPTT', r'C:\DEV__RADIX']


def is_hprof_and_more_1GB(file_name: str) -> bool:
    return '.hprof' in file_name and getsize(file_name) >= 1_000_000_000  # 1 GB


def find_files_by_dir(root_dir: str, match_func) -> list:
    print(f'Start check: {root_dir!r}')

    items = []
    t = default_timer()

    for root, dirs, files in walk(root_dir):
        for f in files:
            file_name = join(root, f)
            file_size = getsize(file_name)
            if match_func(file_name):
                text = f'"{file_name}" {sizeof_fmt(file_size)} ({file_size} bytes)'
                print(text)
                items.append(text)

    print(f'Finish check: {root_dir!r}. Elapsed: {default_timer() - t:.3f} secs')

    return items


def find_files_by_dirs(dirs: list, match_func=is_hprof_and_more_1GB) -> list:
    items = []

    with ThreadPool() as pool:
        for result in pool.map(lambda root_dir: find_files_by_dir(root_dir, match_func), dirs):
            items += result

    return items


if __name__ == '__main__':
    items = find_files_by_dirs(DIRS)

    print()
    print(f'Result ({len(items)}):')
    print('\n'.join(items))
