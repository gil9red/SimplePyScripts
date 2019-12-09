#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import unicodedata
from urllib.parse import urljoin
from typing import List, Tuple
import time

from bs4 import BeautifulSoup
import requests

from common import smart_comparing_names


_CACHE__GAME_GENRES = dict()

# Ссылки из этого кеша не будем грузить
_CACHE__NO_LOAD = []


def search_game_genres(game_name: str, strong=True) -> List[Tuple[str, List[str]]]:
    print(f'[+] Search {game_name!r}...')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
    }

    session = requests.session()
    session.headers.update(headers)

    url = f'https://www.mobygames.com/search/quick?q={game_name}&p=3&search=Go&sFilter=1&sG=on'
    rs = session.get(url)
    if not rs.ok:
        print(f'  [-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
        return []

    root = BeautifulSoup(rs.content, 'html.parser')

    items = []

    for game_block_preview in root.select('.searchTitle > a'):
        title = game_block_preview.get_text(strip=True)

        # Если поиск строгий, то фильтрация по имени выполняетс сразу же. Не будет захода по ссылке
        # Это ускорит парсинг, уменьшит ложные результаты
        if strong and not smart_comparing_names(title, game_name):
            continue

        href = game_block_preview['href']
        url_game = urljoin(rs.url, href)
        if url_game in _CACHE__GAME_GENRES:
            cache = _CACHE__GAME_GENRES[url_game]
            items.append(cache)
            print(f'  [+] Found cache of {url_game!r}, skip load. Cache: {cache}')
            continue

        if url_game in _CACHE__NO_LOAD:
            print(f'  [+] Found cache unnecessary of {url_game!r}, skip load.')
            continue

        print(f'  [+] Load {url_game!r}')

        rs = session.get(url_game)
        if not rs.ok:
            print(f'    [-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
            continue

        game_block = BeautifulSoup(rs.content, 'html.parser')

        genres = game_block\
            .select_one('#coreGameGenre').find_next('div', text='Genre')\
            .find_next_sibling('div').find_all('a')

        # unicodedata.normalize для удаления \xa0 и подобных символов-заменителей
        genres = [unicodedata.normalize("NFKD", a.get_text(strip=True)) for a in genres]

        items.append(
            (title, genres)
        )
        _CACHE__GAME_GENRES[url_game] = (title, genres)

        time.sleep(1)

    return items


def get_game_genres(game_name: str, logs=False) -> List[str]:
    logs and print(f'[+] Search {game_name!r}...')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
    }

    session = requests.session()
    session.headers.update(headers)

    url = f'https://www.mobygames.com/search/quick?q={game_name}&p=3&search=Go&sFilter=1&sG=on'
    rs = session.get(url)
    if not rs.ok:
        print(f'  [-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
        return []

    root = BeautifulSoup(rs.content, 'html.parser')

    for game_block_preview in root.select('.searchTitle > a'):
        title = game_block_preview.get_text(strip=True)

        if not smart_comparing_names(title, game_name):
            continue

        href = game_block_preview['href']
        url_game = urljoin(rs.url, href)
        if url_game in _CACHE__GAME_GENRES:
            cache = _CACHE__GAME_GENRES[url_game]
            print(f'  [+] Found cache of {url_game!r}, skip load. Cache: {cache}')
            return cache

        if url_game in _CACHE__NO_LOAD:
            print(f'  [+] Found cache unnecessary of {url_game!r}, skip load.')
            continue

        logs and print(f'  [+] Load {url_game!r}')

        rs = session.get(url_game)
        if not rs.ok:
            print(f'    [-] Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
            return []

        game_block = BeautifulSoup(rs.content, 'html.parser')

        genres = game_block\
            .select_one('#coreGameGenre').find_next('div', text='Genre')\
            .find_next_sibling('div').find_all('a')

        # unicodedata.normalize для удаления \xa0 и подобных символов-заменителей
        genres = [unicodedata.normalize("NFKD", a.get_text(strip=True)) for a in genres]

        _CACHE__GAME_GENRES[url_game] = genres

        # Сойдет первый, совпадающий по имени, вариант
        return genres

    return []


if __name__ == '__main__':
    from common import _common_test
    _common_test(False, get_game_genres)

    # Search 'Hellgate: London'...
    # Genres: ['Role-Playing (RPG)']
    #
    # --------------------
    #
    # Search 'The Incredible Adventures of Van Helsing'...
    # Genres: ['Action', 'Role-Playing (RPG)']
    #
    # --------------------
    #
    # Search 'Dark Souls: Prepare to Die Edition'...
    # Genres: ['Action', 'Role-Playing (RPG)']
    #
    # --------------------
    #
    # Search 'Twin Sector'...
    # Genres: ['Action']
    #
    # --------------------
    #
    # Search 'Call of Cthulhu: Dark Corners of the Earth'...
    # Genres: ['Action']
    #
    # --------------------
