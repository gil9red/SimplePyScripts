#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from common import RegistryKey


PATHS = [
    r"HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall",
    r"HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall",
    r"HKCU\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
    r"HKLM\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
]

programs = []

for path in PATHS:
    key = RegistryKey.get_or_none(path)
    if not key:
        continue

    for sub_key in key.subkeys():
        name = sub_key.get_str_value('DisplayName')
        if not name:
            continue

        programs.append([
            name,
            sub_key.get_str_value('DisplayVersion'),
            sub_key.get_str_value('Publisher'),
            sub_key.get_str_value('InstallDate'),
            sub_key.name,  # GUID
        ])

# Sort by InstallDate
programs.sort(key=lambda x: x[3], reverse=True)

for i, (name, version, publisher, install_date, _) in enumerate(programs, 1):
    print(f'{i}. {name!r}, {version!r}, {publisher!r}, {install_date!r}')
