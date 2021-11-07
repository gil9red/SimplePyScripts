#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List
from common import get_all_bookmarks


def get_all_pretty_title_of_bookmarks() -> List[str]:
    items = []
    for bookmarks in get_all_bookmarks().values():
        items += [
            x.get_title_with_tags()
            for x in bookmarks
        ]

    return items


if __name__ == '__main__':
    all_bookmarks = get_all_pretty_title_of_bookmarks()
    print('Total bookmarks:', len(all_bookmarks))
    # Total bookmarks: 143

    print()

    for i, bookmark_title in enumerate(all_bookmarks, 1):
        print(f'{i}. {bookmark_title}')

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
