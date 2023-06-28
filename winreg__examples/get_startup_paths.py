#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from fnmatch import fnmatch
from pathlib import Path

from common import RegistryKey


PATHS = [
    (r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders", "Common Startup"),
    (r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders", "Common AltStartup"),
    (r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders", "Common Startup"),
    (r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders", "Common AltStartup"),

    (r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders", "Startup"),
    (r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders", "AltStartup"),
    (r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders", "Startup"),
    (r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders", "AltStartup"),
]

DEFAULT_IGNORED_BY_MASK = ("*.ini",)


def get_path_files(path: Path, ignored_by_mask=DEFAULT_IGNORED_BY_MASK) -> list[Path]:
    items = []
    if path and path.exists():
        for file in path.iterdir():
            if not file.is_file() or any(
                fnmatch(file.name, mask) for mask in ignored_by_mask
            ):
                continue

            items.append(file)

    return items


def get_path_by_files(ignored_by_mask=DEFAULT_IGNORED_BY_MASK) -> dict[str, list[Path]]:
    path_by_files = dict()

    for key_path, value in PATHS:
        key = RegistryKey(key_path)
        path = key.get_path_value(value)
        path_by_files[f"{key.path}, {value}"] = get_path_files(path, ignored_by_mask)

    return path_by_files


def get_all_files(ignored_by_mask=DEFAULT_IGNORED_BY_MASK) -> list[Path]:
    items = []

    for files in get_path_by_files(ignored_by_mask).values():
        for file in files:
            if file not in items:
                items.append(file)

    return items


if __name__ == "__main__":
    all_files = get_all_files()
    print(f"All files ({len(all_files)}):")
    for i, file in enumerate(all_files, 1):
        print(f'  {i:2}. "{file}"')
