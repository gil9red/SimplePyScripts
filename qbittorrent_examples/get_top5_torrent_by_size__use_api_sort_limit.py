#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import sizeof_fmt, get_client


qb = get_client()

torrents_max_top5 = qb.torrents(sort="size", reverse="true", limit="5")
torrents_min_top5 = qb.torrents(sort="size", limit="5")

print("Max top5:")
for i, torrent in enumerate(torrents_max_top5, 1):
    print(
        f"    {i}. {torrent['name']} ({sizeof_fmt(torrent['total_size'])})"
    )

print()

print("Min top5:")
for i, torrent in enumerate(torrents_min_top5, 1):
    print(
        f"    {i}. {torrent['name']} ({sizeof_fmt(torrent['total_size'])})"
    )
