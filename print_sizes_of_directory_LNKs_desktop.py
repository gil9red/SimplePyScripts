#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os

from collections import defaultdict
from glob import iglob

# pip install winshell
import winshell

from human_byte_size import sizeof_fmt


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/b6ac435ee171e48ed35044e8e61e199de641a6e7/get_dir_total_size__using_glob.py
def get_dir_total_size(dir_name: str) -> tuple[int, str]:
    total_size = 0

    for file_name in iglob(dir_name + "/**/*", recursive=True):
        try:
            if os.path.isfile(file_name):
                total_size += os.path.getsize(file_name)

        except Exception as e:
            print(f'File: "{file_name}", error: "{e}"')

    return total_size, sizeof_fmt(total_size)


disc_by_number = defaultdict(int)

path_desktop_lnk = os.path.expanduser(r"~\Desktop\Пройдено\*.lnk")

paths = []

for file_name in iglob(path_desktop_lnk, recursive=True):
    shortcut = winshell.shortcut(file_name)
    path = shortcut.path

    if path.endswith(".exe") and os.path.isfile(path):
        path = os.path.dirname(path)
        paths.append(path)

total_size = 0
total_size_by_disc = defaultdict(int)

total_items = []
disc_by_total_items = defaultdict(list)

paths = sorted(set(paths))

for file_name in paths:
    size, size_str = get_dir_total_size(file_name)
    print(f"{size:<15} {size_str:10} {file_name}")

    total_size += size
    disc = file_name[0]
    total_size_by_disc[disc] += size

    total_items.append((size, size_str, file_name))
    disc_by_total_items[disc].append((size, size_str, file_name))

print()
print(f"Total size: {total_size} {sizeof_fmt(total_size)}")

for disc in sorted(total_size_by_disc):
    size = total_size_by_disc[disc]
    print(f"    {disc} {size:<15} {sizeof_fmt(size)}")

print()
print("Top all:")
items = sorted(total_items, key=lambda x: x[0], reverse=True)
for size, size_str, file_name in items[:5]:
    print(f"    {size:<15} bytes {size_str:10} {file_name}")

print()

for disc, total_items in disc_by_total_items.items():
    print(f"Top of {disc}:")
    for size, size_str, file_name in sorted(
        total_items, key=lambda x: x[0], reverse=True
    )[:3]:
        print(f"    {size:<15} bytes {size_str:10} {file_name}")

    print()
