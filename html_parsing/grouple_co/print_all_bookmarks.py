#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import get_all_bookmarks


status_by_bookmarks = get_all_bookmarks()
print(
    "Total bookmarks:",
    sum(len(bookmarks) for bookmarks in status_by_bookmarks.values()),
)
# Total bookmarks: 143

print()

for status, bookmarks in status_by_bookmarks.items():
    print(f"{status.value}. Bookmarks ({len(bookmarks)}):")
    for i, bookmark in enumerate(bookmarks, 1):
        print(f"{i}. {bookmark}")

    print()

"""
WATCHING. Bookmarks (28):
1. Bookmark(title='Башня Бога', url='https://readmanga.io/bashnia_boga__A339d2', tags=[])
...
28. Bookmark(title='Фейри Тейл. Начало', url='https://readmanga.io/feiri_teil__nachalo', tags=['переведено', 'без глав'])

USER_DEFINED. Bookmarks (0):

ON_HOLD. Bookmarks (4):
1. Bookmark(title='Д.Грэй-мен', url='https://readmanga.io/d_grei_men__A5327', tags=[])
...
4. Bookmark(title='Четыре рыцаря', url='https://readmanga.io/chetyre_rycaria__A5327', tags=[])

PLANED. Bookmarks (56):
1. Bookmark(title='"Сверхъестественное" для чайников', url='https://readmanga.io/_sverhestestvennoe__dlia_chainikov', tags=['сингл'])
...
56. Bookmark(title='Энигма', url='https://readmanga.io/enigma__A5274', tags=['переведено'])

COMPLETED. Bookmarks (55):
1. Bookmark(title='666 Сатана', url='https://readmanga.io/666_satana__A533b', tags=['переведено'])
...
55. Bookmark(title='Я — герой!', url='https://mintmanga.live/ia___geroi___A5327', tags=['переведено'])

FAVORITE. Bookmarks (0):
"""
