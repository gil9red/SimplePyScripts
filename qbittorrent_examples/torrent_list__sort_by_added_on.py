#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/qbittorrent/qbittorrent/wiki/WebUI-API-Documentation#get-torrent-list


from common import get_client, sizeof_fmt


qb = get_client()
torrents = qb.torrents(sort='added_on', reverse='true')

total_size = 0

for i, torrent in enumerate(torrents, 1):
    torrent_size = torrent['total_size']
    total_size += torrent_size

    print('{:<3} {} ({})'.format(i, torrent['name'], sizeof_fmt(torrent_size)))

print()
print('Total torrents: {}, total size: {} ({} bytes)'.format(len(torrents), sizeof_fmt(total_size), total_size))
