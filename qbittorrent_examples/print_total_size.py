#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import get_client, sizeof_fmt


qb = get_client()

torrents = qb.torrents()
total_size = sum(torrent["total_size"] for torrent in torrents)

print(f"Total torrents: {len(torrents)}")
print(f"Total size:     {sizeof_fmt(total_size)} ({total_size} bytes)")
