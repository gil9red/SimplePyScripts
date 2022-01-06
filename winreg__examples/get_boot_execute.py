#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://www.saule-spb.ru/library/autorun.html


from typing import Dict, List
from common import get_entry


PATHS = [
    (r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager", "BootExecute"),
    (r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager", "Execute"),
    (r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager", "SetupExecute"),
]


def get_boot_execute() -> Dict[str, List[str]]:
    name_by_value = dict()
    for path, name in PATHS:
        entry = get_entry(path, name)
        name_by_value[name] = entry.value if entry else []
    return name_by_value


if __name__ == '__main__':
    print(get_boot_execute())

