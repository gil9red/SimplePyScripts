#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import get_client, print_torrents


def get_torrents(qb, search_name="", **filters) -> list:
    def match(name: str) -> bool:
        return search_name.lower() in name.lower()

    return [torrent for torrent in qb.torrents(**filters) if match(torrent["name"])]


qb = get_client()
torrents = get_torrents(qb, search_name=".mkv")
print_torrents(torrents)
