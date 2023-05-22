#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import get_plain_all_bookmarks_from_user


bookmarks = get_plain_all_bookmarks_from_user(315828)
print(f"Bookmarks ({len(bookmarks)}):")
for i, bookmark in enumerate(bookmarks, 1):
    print(f"{i}. {bookmark}")
"""
Bookmarks (85):
1. Bookmark(title='Башня Бога', url='https://readmanga.io/bashnia_boga__A339d2', tags=[])
2. Bookmark(title='Берсерк', url='https://readmanga.io/berserk', tags=[])
3. Bookmark(title='Боруто', url='https://readmanga.io/boruto__A5327', tags=[])
...
83. Bookmark(title='Школа мертвецов', url='/internal/red/14905', tags=['переведено'])
84. Bookmark(title='Школьный эфир!', url='https://readmanga.io/love_live__dj___school_live', tags=['сингл'])
85. Bookmark(title='Энигма', url='https://readmanga.io/enigma__A5274', tags=['переведено'])
"""
