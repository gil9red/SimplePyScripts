#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import time

from common import RegistryKey


key = RegistryKey(r'HKEY_CURRENT_USER\Software\SigmaTeam\AlienShooter2LegendPC')
name_by_value = key.get_str_values_as_dict()

while True:
    modified_keys = []

    for v in key.values():
        name = v.name

        if name_by_value.get(name) != v.value:
            modified_keys.append(name)
            name_by_value[name] = v.value

    if modified_keys:
        print(DT.datetime.now())
        print(*modified_keys, sep='\n')
        print()

    time.sleep(5)
