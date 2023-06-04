#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import get_client


qb = get_client()

created_by_list = set()

for torrent in qb.torrents():
    created_by = qb.get_torrent(torrent["hash"])["created_by"]
    if created_by:
        created_by_list.add(created_by)

print("\n".join(created_by_list))
