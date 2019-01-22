#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from collections import defaultdict
from glob import iglob
import os

# pip install winshell
import winshell


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)

        num /= 1024.0

    return "%3.1f %s" % (num, 'TB')


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/b6ac435ee171e48ed35044e8e61e199de641a6e7/get_dir_total_size__using_glob.py
def get_dir_total_size(dir_name: str) -> (int, str):
    total_size = 0

    for file_name in iglob(dir_name + '/**/*', recursive=True):
        try:
            if os.path.isfile(file_name):
                total_size += os.path.getsize(file_name)

        except Exception as e:
            print('File: "{}", error: "{}"'.format(file_name, e))

    return total_size, sizeof_fmt(total_size)


disc_by_number = defaultdict(int)

path_desktop_lnk = os.path.expanduser(r'~\Desktop\**\*.lnk')

paths = []

for file_name in iglob(path_desktop_lnk, recursive=True):
    shortcut = winshell.shortcut(file_name)
    path = shortcut.path

    if path.endswith('.exe') and os.path.isfile(path):
        path = os.path.dirname(path)
        paths.append(path)

total_size = 0
total_size_by_disc = defaultdict(int)

paths = sorted(set(paths))

for file_name in paths:
    size, size_str = get_dir_total_size(file_name)
    print('{:<15} {:10} {}'.format(size, size_str, file_name))

    total_size += size
    total_size_by_disc[file_name[0]] += size

print()
print('Total size:', total_size, sizeof_fmt(total_size))

for disc in sorted(total_size_by_disc):
    size = total_size_by_disc[disc]
    print(disc, size, sizeof_fmt(size))
