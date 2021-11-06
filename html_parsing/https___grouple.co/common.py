#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import enum
import time
from dataclasses import dataclass, field
from typing import List, Dict

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

        time.sleep(1)

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


def get_all_bookmarks() -> Dict[Status, List[Bookmark]]:
    return {
        status: get_bookmarks_by_status(status)
        for status in Status
    }


if __name__ == '__main__':
    assert Status.WATCHING.name == Status.WATCHING.value
    assert Status.WATCHING.name == "WATCHING"

    print(session.cookies)
    print(do_auth())
    print(session.cookies)

    print('\n' + '-' * 50 + '\n')

    status_by_bookmarks = get_all_bookmarks()
    print('Total bookmarks:', sum(len(bookmarks) for bookmarks in status_by_bookmarks.values()))
    # Total bookmarks: 143

    for status, bookmarks in status_by_bookmarks.items():
        print(f'{status.value}. Bookmarks ({len(bookmarks)}):')
        for i, bookmark in enumerate(bookmarks, 1):
            print(f'{i}. {bookmark}')

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

    print('\n' + '-' * 50 + '\n')

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