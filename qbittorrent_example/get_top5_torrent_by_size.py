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

    torrents_max_top5 = sorted(torrents, key=lambda x: x['total_size'], reverse=True)[:5]
    torrents_min_top5 = sorted(torrents, key=lambda x: x['total_size'])[:5]

    print('Max top5:')

    for i, torrent in enumerate(torrents_max_top5, 1):
        print('    {}. {} ({})'.format(i, torrent['name'], sizeof_fmt(torrent['total_size'])))

    print()

    print('Min top5:')

    for i, torrent in enumerate(torrents_min_top5, 1):
        print('    {}. {} ({})'.format(i, torrent['name'], sizeof_fmt(torrent['total_size'])))
