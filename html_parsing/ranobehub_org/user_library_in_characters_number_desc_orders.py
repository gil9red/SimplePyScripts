#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

from get_bookmarks import get_bookmarks
from get_ranobe_info import get_ranobe_info, Ranobe

USER_ID: int = 19803

items: list[tuple[str, Ranobe]] = []
for bookmark in get_bookmarks(USER_ID):
    ranobe = get_ranobe_info(bookmark.url)
    items.append((bookmark.status, ranobe))
    time.sleep(1)

items.sort(key=lambda x: x[1].characters, reverse=True)

for i, (bookmark_status, ranobe) in enumerate(items, 1):
    print(f'{i:3}. {ranobe.characters_str}, "{ranobe.title}" [{bookmark_status}]')
"""
  1. 27850633, "Преподобный Гу" [Запланировано]
  2. 27279603, "Во всеоружии" [Запланировано]
  3. 24896496, "Сильнейшая Система Убийцы Драконов" [Запланировано]
  4. 23589252, "Чернокнижник в Мире Магов" [Прочитано]
  5. 23113448, "Пространственная ферма в ином мире" [Запланировано]
  6. 22335714, "Противостояние Святого" [Запланировано]
  7. 19747148, "Маг на полную ставку" [Запланировано]
  8. 18252056, "Легендарный механик" [Запланировано]
  9. 17883942, "Легендарный лунный скульптор" [Прочитано]
 10. 17009477, "Расколотая битвой синева небес" [Запланировано]
 ...
 64. 9358, "Я не отдам его какой-то “Святой”!" [Прочитано]
 65. 8272, "Я попала в игру для девочек, но стала слишком злой" [Прочитано]
 66. 24, "Комната ведьмы Апреля" [Прочитано]
"""
