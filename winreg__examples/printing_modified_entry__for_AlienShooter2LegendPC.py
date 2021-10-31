#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import time

from common import get_entries


KEY = r'HKEY_CURRENT_USER\Software\SigmaTeam\AlienShooter2LegendPC'


name_by_value = {
    entry.name: entry.value for entry in get_entries(KEY)
}

while True:
    modified_keys = []

    for entry in get_entries(KEY):
        name = entry.name

        if name_by_value.get(name) != entry.value:
            modified_keys.append(name)
            name_by_value[name] = entry.value

    if modified_keys:
        print(DT.datetime.now())
        print(*modified_keys, sep='\n')
        print()

    time.sleep(5)
