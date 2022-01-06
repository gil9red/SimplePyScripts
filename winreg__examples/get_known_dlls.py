#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import Dict
from common import get_entries_as_dict


PATH = r'HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\KnownDLLs'


def get_known_dlls() -> Dict[str, str]:
    return get_entries_as_dict(PATH, raw_value=True)


if __name__ == '__main__':
    print(get_known_dlls())

