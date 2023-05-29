#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from os import listdir
from os.path import join, getsize, isfile

# pip install humanize
from humanize import naturalsize as sizeof_fmt


def get_dir_total_size(dir_name: str, ignore_permission_error=True) -> tuple[int, str]:
    def _get_sub_size(root_path: str) -> int:
        if isfile(root_path):
            return getsize(root_path)

        total_size = 0

        try:
            for path in listdir(root_path):
                abs_path = join(root_path, path)

                if isfile(abs_path):
                    size = getsize(abs_path)
                else:
                    size = _get_sub_size(abs_path)

                total_size += size

        except Exception as e:
            if type(e) is PermissionError:
                if not ignore_permission_error:
                    print(f'Error: "{e}"')
            else:
                print(f'Path: "{root_path}", error: "{e}"')

        return total_size

    total_size = _get_sub_size(dir_name)
    return total_size, sizeof_fmt(total_size)


if __name__ == "__main__":
    import os

    # paths = [r"C:\Users\Default", r"C:\Program Files (x86)", os.path.expanduser(r'~\Desktop')]
    paths = [".."]

    for path in paths:
        path = os.path.abspath(path)

        size, size_str = get_dir_total_size(path)
        print(f'"{path}": {size} bytes / {size_str}')
