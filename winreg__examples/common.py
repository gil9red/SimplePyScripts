#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import winreg

from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path
from winreg import QueryInfoKey, EnumValue, OpenKey, HKEYType


@dataclass
class Entry:
    name: str
    value: str
    type: int


def expand_registry_key(key: str) -> str:
    return {
        'HKCU': 'HKEY_CURRENT_USER',
        'HKLM': 'HKEY_LOCAL_MACHINE',
    }.get(key, key)


def get_key(path: str) -> Optional[HKEYType]:
    # Example:
    #     path = r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
    #     registry_key_name = "HKEY_LOCAL_MACHINE"
    #     relative_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
    registry_key_name, relative_path = path.split('\\', maxsplit=1)
    registry_key_name = expand_registry_key(registry_key_name)

    registry_key = getattr(winreg, registry_key_name)

    try:
        return OpenKey(registry_key, relative_path)
    except:
        return


def get_entries(path: str, expand_vars=True) -> List[Entry]:
    items = []

    key = get_key(path)
    if not key:
        return items

    _, number_of_values, _ = QueryInfoKey(key)
    for i in range(number_of_values):
        name, value, type_value = EnumValue(key, i)
        value = str(value)
        if expand_vars:
            value = os.path.expandvars(value)

        items.append(
            Entry(name, value, type_value)
        )

    return items


def get_entry(path: str, value: str, expand_vars=True) -> Optional[Entry]:
    for entry in get_entries(path, expand_vars):
        if entry.name == value:
            return entry


def get_entry_path(path: str, name: str) -> Optional[Path]:
    entry = get_entry(path, name)
    if not entry:
        return

    return Path(entry.value)


if __name__ == '__main__':
    assert get_key(r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
    assert get_key(r"HKLM\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")

    assert get_key(r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
    assert get_key(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
