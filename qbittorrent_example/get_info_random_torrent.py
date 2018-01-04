#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')


# pip install python-qbittorrent
from qbittorrent import Client
from config import IP_HOST, USER, PASSWORD

qb = Client(IP_HOST)
qb.login(USER, PASSWORD)

import random
torrent = random.choice(qb.torrents())
print('{} ({})'.format(torrent['name'], sizeof_fmt(torrent['total_size'])))

files = qb.get_torrent_files(torrent['hash'])
print('Files ({}):'.format(len(files)))

for file in sorted(files, key=lambda x: x['name']):
    print('    {} ({})'.format(file['name'], sizeof_fmt(file['size'])))
