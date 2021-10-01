#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from fnmatch import fnmatch
from pathlib import Path
from typing import Tuple, List, Optional

from common import get_entry_path


PATHS = [
    (r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders', 'Common Startup'),
    (r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders', 'Common AltStartup'),
    (r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders', 'Common Startup'),
    (r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders', 'Common AltStartup'),

    (r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders', 'Startup'),
    (r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders', 'AltStartup'),
    (r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders', 'Startup'),
    (r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders', 'AltStartup'),
]


def get_path_files(path: Path, ignored_by_mask=('*.ini',)) -> List[Path]:
    items = []
    if path and path.exists():
        for file in path.iterdir():
            if not file.is_file() or any(fnmatch(file.name, mask) for mask in ignored_by_mask):
                continue

            items.append(file)

    return items


def get_all_files(ignored_by_mask=('*.ini',)) -> List[Path]:
    items = []

    for key_path, value in PATHS:
        path = get_entry_path(key_path, value)

        for file in get_path_files(path, ignored_by_mask):
            if file not in items:
                items.append(file)

    return items


if __name__ == '__main__':
    for key_path, value in PATHS:
        path = get_entry_path(key_path, value)
        print(fr'{key_path}\{value} = {path}')

        files = get_path_files(path)
        print(f'    Files ({len(files)}): {files}')

    print()

    all_files = get_all_files()
    print(f'All files ({len(all_files)}): {all_files}')
