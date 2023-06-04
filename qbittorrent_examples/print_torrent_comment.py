#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import get_client


def get_comment(torrent):
    return qb.get_torrent(torrent["hash"])["comment"]


qb = get_client()

comment_list = []

for torrent in qb.torrents():
    comment = get_comment(torrent)
    if comment:
        comment_list.append(comment)

comment_list.sort()
print("\n".join(comment_list))
