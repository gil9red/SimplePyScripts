#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://www.saule-spb.ru/library/autorun.html


from common import RegistryKey


ROOT_PATH = r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager"
PATHS = [
    (ROOT_PATH, "BootExecute"),
    (ROOT_PATH, "Execute"),
    (ROOT_PATH, "SetupExecute"),
]


def get_boot_execute() -> dict[str, list[str]]:
    key_by_value = dict()
    for path, name in PATHS:
        key = RegistryKey.get_or_none(path)
        if not key:
            continue

        if value := key.get_str_value(name):
            key_by_value[f"{key.path}, {name}"] = value

    return key_by_value


if __name__ == "__main__":
    print(get_boot_execute())
    # {'HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Session Manager, BootExecute': ['autocheck autochk /m /P \\Device\\HarddiskVolume10', 'autocheck autochk /m /P \\Device\\HarddiskVolume38', 'autocheck autochk /m /P \\Device\\HarddiskVolume30', 'autocheck autochk *']}
