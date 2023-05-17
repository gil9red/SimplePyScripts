#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from glob import iglob, escape
import os

from common import sizeof_fmt


# FIXME: glob ignored dot folders and files
#        Examples: .git/ .idea/ .gitignore
def get_dir_total_size(dir_name: str) -> (int, str):
    total_size = 0

    for file_name in iglob(escape(dir_name) + "/**", recursive=True):
        try:
            if os.path.isfile(file_name):
                total_size += os.path.getsize(file_name)

        except Exception as e:
            print(f'File: "{file_name}", error: "{e}"')

    return total_size, sizeof_fmt(total_size)


if __name__ == "__main__":
    # paths = [r"C:\Users\Default", r"C:\Program Files (x86)", os.path.expanduser(r'~\Desktop')]
    paths = [".."]

    for path in paths:
        path = os.path.abspath(path)

        size, size_str = get_dir_total_size(path)
        print(f'"{path}": {size} bytes / {size_str}')
