#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://www.saule-spb.ru/library/autorun.html
# SOURCE: http://datadump.ru/virus-detection/


from common import RegistryKey


PATHS = [
    (r"HKLM\Software\Microsoft\Command Processor", "AutoRun"),
    (r"HKCU\Software\Microsoft\Command Processor", "AutoRun"),
]


def get_command_processor() -> dict[str, str]:
    path_by_value = dict()
    for path, name in PATHS:
        key = RegistryKey.get_or_none(path)
        if not key:
            continue

        if value := key.get_str_value(name):
            path_by_value[fr'{key.path}, {name}'] = value

    return path_by_value


if __name__ == '__main__':
    print(get_command_processor())
