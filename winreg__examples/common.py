#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import winreg

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union, Any
from pathlib import Path
from winreg import QueryInfoKey, EnumKey, EnumValue, OpenKey, HKEYType


@dataclass
class Entry:
    name: str
    value: Any
    type: int


def expand_registry_key(key: str) -> str:
    return {
        'HKCU': 'HKEY_CURRENT_USER',
        'HKLM': 'HKEY_LOCAL_MACHINE',
    }.get(key, key)


def expand_path(path: str) -> str:
    registry_key_name, relative_path = path.split('\\', maxsplit=1)
    registry_key_name = expand_registry_key(registry_key_name)

    return fr'{registry_key_name}\{relative_path}'


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


def get_entries(path: Union[str, HKEYType], expand_vars=True) -> List[Entry]:
    items = []

    if isinstance(path, HKEYType):
        key = path
    else:
        key = get_key(path)

    if not key:
        return items

    _, number_of_values, _ = QueryInfoKey(key)
    for i in range(number_of_values):
        name, value, type_value = EnumValue(key, i)

        if expand_vars and isinstance(value, str):
            value = os.path.expandvars(value)

        items.append(
            Entry(name, value, type_value)
        )

    return items


def get_entries_as_dict(path: Union[str, HKEYType], raw_value=False, expand_vars=True) -> Dict[str, Union[Entry, Any]]:
    return {
        entry.name: entry.value if raw_value else entry
        for entry in get_entries(path, expand_vars)
    }


def get_entry(path: str, name: str, expand_vars=True) -> Optional[Entry]:
    for entry in get_entries(path, expand_vars):
        if entry.name.upper() == name.upper():
            return entry


def get_subkeys(path: str) -> List[Tuple[str, HKEYType]]:
    items = []

    key = get_key(path)
    if not key:
        return items

    number_of_subkeys, _, _ = QueryInfoKey(key)
    for i in range(number_of_subkeys):
        sub_key_name = EnumKey(key, i)
        sub_key = OpenKey(key, sub_key_name)

        items.append((sub_key_name, sub_key))

    return items


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

    assert expand_path(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run") \
           == r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run"
