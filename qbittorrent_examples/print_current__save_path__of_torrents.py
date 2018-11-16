#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from collections import Counter
from common import get_client, print_table


qb = get_client()

items = [torrent['save_path'] for torrent in qb.torrents()]
print('Save path: ', sorted(set(items)))

for name, number in Counter(items).items():
    print('"{}": {}'.format(name, number))
