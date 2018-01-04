#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')


if __name__ == '__main__':
    # pip install python-qbittorrent
    from qbittorrent import Client
    from config import IP_HOST, USER, PASSWORD

    qb = Client(IP_HOST)
    qb.login(USER, PASSWORD)

    torrents = qb.torrents()
    total_size = 0

    for i, torrent in enumerate(torrents, 1):
        torrent_size = torrent['total_size']
        total_size += torrent_size

        print('{:<3} {} ({})'.format(i, torrent['name'], sizeof_fmt(torrent_size)))

    print('\n')
    print('Total torrents: {}, total size: {} ({} bytes)'.format(len(torrents), sizeof_fmt(total_size), total_size))
