#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random
from common import get_client, sizeof_fmt, print_files_table


qb = get_client()
torrent = random.choice(qb.torrents())
print(f"{torrent['name']} ({sizeof_fmt(torrent['total_size'])})")
print()

files = qb.get_torrent_files(torrent["hash"])
print(f"Files ({len(files)}):")

print_files_table(files)
