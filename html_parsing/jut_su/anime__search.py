#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from dataclasses import dataclass
from typing import List
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from common import session


@dataclass
class Anime:
    url: str
    title: str


def search(text: str) -> List[Anime]:
    data = {
        'ajax_load': 'yes',
        'start_from_page': 1,
        'show_search': text,
        'anime_of_user': '',
    }
    headers = {
        'X-Requested-With': 'XMLHttpRequest',  # AJAX
    }
    rs = session.post('https://jut.su/anime/', headers=headers, data=data)
    rs.raise_for_status()

    items = []
    root = BeautifulSoup(rs.text, 'html.parser')
    for anime_el in root.select('.all_anime_global'):
        url = urljoin(rs.url, anime_el.a['href'])
        title = anime_el.select_one('.aaname').text

        items.append(Anime(url, title))

    return items


if __name__ == '__main__':
    for anime in search(text='гора'):
        print(anime)
    """
    Anime(url='https://jut.su/shiki/', title='Усопшие')
    Anime(url='https://jut.su/slime-taoshite-300-nen/', title='Убивала слизней 300 лет до максимального уровня')
    Anime(url='https://jut.su/reikenzan/', title='Гора Священного меча')
    Anime(url='https://jut.su/shakunetsu-kabaddi/', title='Пылающий Кабадди')
    """
