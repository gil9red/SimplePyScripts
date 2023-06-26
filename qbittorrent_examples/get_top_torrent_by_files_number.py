#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import sizeof_fmt, get_client, print_files_table


qb = get_client()

torrents = qb.torrents()
torrent = max(torrents, key=lambda x: len(qb.get_torrent_files(x["hash"])))

print(f"{torrent['name']} ({sizeof_fmt(torrent['total_size'])})")
print()

files = qb.get_torrent_files(torrent["hash"])
print(f"Files ({len(files)}):")

print_files_table(files)
