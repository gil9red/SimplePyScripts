#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://www.saule-spb.ru/library/autorun.html
# SOURCE: http://datadump.ru/virus-detection/


from typing import Dict, Optional
from common import get_entry


PATHS = [
    (r"HKLM\Software\Microsoft\Command Processor", "AutoRun"),
    (r"HKCU\Software\Microsoft\Command Processor", "AutoRun"),
]


def get_command_processor() -> Dict[str, Optional[str]]:
    path_by_value = dict()
    for path, name in PATHS:
        entry = get_entry(path, name)
        path_by_value[fr'{path}\{name}'] = entry.value if entry else None

    return path_by_value


if __name__ == '__main__':
    print(get_command_processor())
