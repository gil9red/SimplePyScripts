#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import random
from common import get_client, sizeof_fmt, print_table


qb = get_client()
torrent = random.choice(qb.torrents())
print('{} ({})'.format(torrent['name'], sizeof_fmt(torrent['total_size'])))
print()

files = qb.get_torrent_files(torrent['hash'])
print('Files ({}):'.format(len(files)))

rows = [(file['name'], sizeof_fmt(file['size'])) for file in sorted(files, key=lambda x: x['name'])]
headers = ['#', 'File Name', 'Size']
print_table(rows, headers)
