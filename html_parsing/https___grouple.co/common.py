#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import enum
from dataclasses import dataclass, field
from typing import List

import requests
from bs4 import BeautifulSoup

from config import LOGIN, PASSWORD


@dataclass
class Bookmark:
    title: str
    url: str
    tags: List[str] = field(default_factory=list)


class AutoName(enum.Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class Status(AutoName):
    WATCHING = enum.auto()      # В процессе
    USER_DEFINED = enum.auto()  # Пользовательская
    ON_HOLD = enum.auto()       # Пока бросил
    PLANED = enum.auto()        # В планах
    COMPLETED = enum.auto()     # Готово
    FAVORITE = enum.auto()      # Любимая


session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'


def do_auth() -> requests.Response:
    form_data = {
        'username': LOGIN,
        'password': PASSWORD,
    }

    rs = session.post('https://grouple.co/login/authenticate', data=form_data)
    rs.raise_for_status()

    # Example: https://grouple.co/internal/auth/login?login_error=1
    if 'error' in rs.url:
        raise Exception('Invalid auth!')

    return rs


def load(url: str) -> requests.Response:
    while True:
        rs = session.get(url)
        rs.raise_for_status()

        # Если нужно авторизоваться
        if '/login/auth' in rs.url:
            do_auth()
            continue

        return rs


def get_bookmarks(url: str) -> List[Bookmark]:
    rs = load(url)
    root = BeautifulSoup(rs.content, 'html.parser')

    items = []
    for row in root.select('.bookmark-row a.site-element'):
        tags = []
        if row.sup:
            tags += [x.get_text(strip=True).lower() for x in row.sup.select('span[class]')]

            # Удаление сноски ("Выпуск завершен", "переведено" и т.п.), чтобы в title она не попала
            row.sup.decompose()

        title = row.get_text(strip=True)
        url = row['href']

        items.append(
            Bookmark(title=title, url=url, tags=tags)
        )

    return items


def get_bookmarks_by_status(status: Status) -> List[Bookmark]:
    return get_bookmarks(f'https://grouple.co/private/bookmarks?status={status.value}')


if __name__ == '__main__':
    assert Status.WATCHING.name == Status.WATCHING.value
    assert Status.WATCHING.name == "WATCHING"

    print(session.cookies)
    print(do_auth())
    print(session.cookies)

    print()

    bookmarks = get_bookmarks_by_status(Status.WATCHING)
    print(f'Bookmarks ({len(bookmarks)}):')
    for i, bookmark in enumerate(bookmarks, 1):
        print(f'{i}. {bookmark}')
    """
    Bookmarks (28):
    1. Bookmark(title='Башня Бога', url='https://readmanga.io/bashnia_boga__A339d2', tags=[])
    2. Bookmark(title='Берсерк', url='https://readmanga.io/berserk', tags=[])
    3. Bookmark(title='Боруто', url='https://readmanga.io/boruto__A5327', tags=[])
    ...
    26. Bookmark(title='Священная  земля', url='https://readmanga.io/sviachennaia__zemlia__A533b', tags=['переведено'])
    27. Bookmark(title='Терраформирование', url='https://mintmanga.live/terraformirovanie__A5327', tags=[])
    28. Bookmark(title='Фейри Тейл. Начало', url='https://readmanga.io/feiri_teil__nachalo', tags=['переведено', 'Без глав'])
    """