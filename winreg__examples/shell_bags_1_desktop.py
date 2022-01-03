#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from common import get_entries
from winapi__windows__ctypes.get_screen_info import get_screen_info


width, height, dpi = get_screen_info()

key = r'HKCU\Software\Microsoft\Windows\Shell\Bags\1\Desktop'
entries = get_entries(key)
for entry in entries:
    print(entry)

print()

print(f'ItemPos for current screen:')
for entry in entries:
    name = f'ItemPos{width}x{height}x{dpi}'
    if name in entry.name:
        print(entry)
