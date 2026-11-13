#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

from get_bookmarks import get_bookmarks
from get_ranobe_info import get_ranobe_info

USER_ID: int = 19803

# Приблизительное количество знаков в "Война и мир"
CHARACTERS_NUMBER_OF_METRICS: int = 4_000_000

number: int = 0
total_characters: int = 0
for bookmark in get_bookmarks(USER_ID):
    if bookmark.status != "Прочитано":
        continue

    ranobe = get_ranobe_info(bookmark.url)
    number += 1
    total_characters += ranobe.characters

    time.sleep(1)

print(f"Всего прочитано: {number}")
print(f"Всего знаков: {total_characters:_}".replace("_", " "))
print(
    'Равнозначно прочитанным "Войне и мир": '
    f"{total_characters // CHARACTERS_NUMBER_OF_METRICS}"
)
"""
Всего прочитано: 39
Всего знаков: 148 025 120
Равнозначно прочитанным "Войне и мир": 37
"""
