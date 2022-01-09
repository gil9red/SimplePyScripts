#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from common import RegistryKey
from winapi__windows__ctypes.get_screen_info import get_screen_info


key = RegistryKey(r'HKCU\Software\Microsoft\Windows\Shell\Bags\1\Desktop')
values = key.values()
for v in values:
    print(v)

print()

width, height, dpi = get_screen_info()

print(f'ItemPos for current screen:')
for v in values:
    name = f'ItemPos{width}x{height}x{dpi}'
    if name in v.name:
        print(v)
