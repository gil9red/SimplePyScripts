#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from collections import Counter
from common import get_client


qb = get_client()

items = [torrent["save_path"] for torrent in qb.torrents()]
counter = Counter(items)

print("Save path:", sorted(counter.keys()))

for name, number in counter.items():
    print(f"{name!r}: {number}")
