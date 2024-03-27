#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

from get_bookmarks import get_bookmarks
from get_ranobe_info import get_ranobe_info


USER_ID = 19803

# Приблизительное количество знаков в "Война и мир"
CHARACTERS_NUMBER_OF_METRICS = 4_000_000

number = 0
total_characters_number = 0
for bookmark in get_bookmarks(USER_ID):
    if bookmark.status != "Прочитано":
        continue

    ranobe = get_ranobe_info(bookmark.url)
    number += 1
    total_characters_number += ranobe.characters_number

    time.sleep(1)

print(f"Всего прочитано: {number}")
print(f"Всего знаков: {total_characters_number:_}".replace("_", " "))
print(
    'Равнозначно прочитанным "Войне и мир": '
    f"{total_characters_number // CHARACTERS_NUMBER_OF_METRICS}"
)
"""
Всего прочитано: 35
Всего знаков: 112 119 024
Равнозначно прочитанным "Войне и мир": 28
"""
