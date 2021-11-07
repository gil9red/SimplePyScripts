#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from common import get_all_bookmarks


status_by_bookmarks = get_all_bookmarks()
all_bookmarks = []
for bookmarks in status_by_bookmarks.values():
    all_bookmarks += bookmarks
print('Total bookmarks:', len(all_bookmarks))
# Total bookmarks: 143

print()

for i, bookmark in enumerate(all_bookmarks, 1):
    print(f'{i}. {bookmark.get_title_with_tags()}')

"""
1. Башня Бога
2. Берсерк
3. Боруто
4. Ван Пис [обновлено]
...
139. Фейри Тейл [переведено, без глав]
140. Шаман Кинг - зеро [выпуск завершен]
141. Шухер! У нас новый студент! [переведено]
142. Эльфийская песнь [переведено]
143. Я — герой! [переведено]
"""
