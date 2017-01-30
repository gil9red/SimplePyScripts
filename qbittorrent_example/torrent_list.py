#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    from config import *
    from qbittorrent import Client

    qb = Client(IP_HOST)
    qb.login(USER, PASSWORD)

    for i, torrent in enumerate(qb.torrents(), 1):
        print(i, torrent['name'], torrent['hash'])
