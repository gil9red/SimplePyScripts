#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from winreg import *


UNINSTALL_PATH_LIST = [
    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
    r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
]

programs_dict = dict()

for path in UNINSTALL_PATH_LIST:
    for hkey in [HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER]:
        try:
            key = OpenKey(hkey, path)
        except FileNotFoundError:
            continue

        for i in range(QueryInfoKey(key)[0]):
            keyname = EnumKey(key, i)
            subkey = OpenKey(key, keyname)

            try:
                subkey_dict = dict()
                for j in range(QueryInfoKey(subkey)[1]):
                    k, v = EnumValue(subkey, j)[:2]
                    subkey_dict[k] = v

                if "DisplayName" not in subkey_dict:
                    continue

                name = subkey_dict["DisplayName"].strip()
                if not name:
                    continue

                programs_dict[name] = subkey_dict

            except WindowsError:
                pass


for i, name in enumerate(sorted(programs_dict.keys()), 1):
    subkey_dict = programs_dict[name]
    print(f"{i}. {name}:")
    print(f'    DisplayVersion: {subkey_dict.get("DisplayVersion", "")}')
    print(f'    Publisher: {subkey_dict.get("Publisher", "")}')
    print(f'    InstallDate: {subkey_dict.get("InstallDate", "")}')
    print()
