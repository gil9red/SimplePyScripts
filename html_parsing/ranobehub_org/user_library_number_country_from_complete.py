#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
from collections import Counter

from get_bookmarks import get_bookmarks
from get_ranobe_info import get_ranobe_info


USER_ID = 19803

items: list[str] = []
for bookmark in get_bookmarks(USER_ID):
    if bookmark.status != "Прочитано":
        continue

    ranobe = get_ranobe_info(bookmark.url)

    items.append(ranobe.country)
    time.sleep(1)

for i, (country, number) in enumerate(Counter(items).most_common(), 1):
    print(f'{i}. {country}: {number}')
"""
1. Япония: 21
2. Корея: 8
3. Китай: 4
4. США: 1
"""
