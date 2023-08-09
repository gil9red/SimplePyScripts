#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

from get_bookmarks import get_bookmarks
from get_ranobe_info import get_ranobe_info, Ranobe


USER_ID = 19803

items: list[tuple[str, Ranobe]] = []
for bookmark in get_bookmarks(USER_ID):
    ranobe = get_ranobe_info(bookmark.url)
    items.append((bookmark.status, ranobe))
    time.sleep(1)

items.sort(key=lambda x: x[1].characters_number, reverse=True)

for i, (bookmark_status, ranobe) in enumerate(items, 1):
    print(f'{i}. {ranobe.characters}, "{ranobe.title}" [{bookmark_status}]')
"""
1. 24M, "Сильнейшая Система Убийцы Драконов" [Запланировано]
2. 23M, "Чернокнижник в Мире Магов" [Прочитано]
3. 22M, "Во всеоружии" [Запланировано]
4. 19M, "Маг на полную ставку" [Запланировано]
5. 18M, "Легендарный механик" [Запланировано]
6. 17M, "Легендарный лунный скульптор" [Прочитано]
7. 12M, "Освободите эту Ведьму" [Запланировано]
8. 11M, "Мир Бога и Дьявола" [Прочитано]
9. 11M, "Непутевый ученик в школе магии" [Читаю]
...
41. 22K, "Мой герой" [Прочитано]
42. 9K, "Я не отдам его какой-то “Святой”!" [Прочитано]
43. 8K, "Я попала в игру для девочек, но стала слишком злой" [Прочитано]
"""
