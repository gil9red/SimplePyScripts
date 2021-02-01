#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List

import requests
from bs4 import BeautifulSoup


session = requests.session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'


def get_canonical_characters() -> List[str]:
    url = 'https://onepiece.fandom.com/ru/wiki/Список_канонических_персонажей'

    rs = session.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')

    return [
        td.get_text(strip=True)
        for td in root.select_one('.wikitable').select('tbody > tr > td:nth-of-type(2)')
    ]


def get_dead_characters() -> List[str]:
    url = 'https://onepiece.fandom.com/ru/wiki/Категория:Умершие_персонажи'

    rs = session.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')

    return [
        x.get_text(strip=True)
        for x in root.select('.category-page__member-link')
    ]


if __name__ == '__main__':
    canonical_characters = get_canonical_characters()
    total_canonical_characters = len(canonical_characters)

    dead_canonical_characters = sorted(set(canonical_characters) & set(get_dead_characters()))
    total_dead_canonical_characters = len(dead_canonical_characters)

    print('Total canonical characters:', total_canonical_characters)
    print(
        f'Total dead canonical characters: {total_dead_canonical_characters} '
        f'({total_dead_canonical_characters * 100 / total_canonical_characters:.2f}%)'
    )
    print(
        f'[{", ".join(map(repr, dead_canonical_characters[:3]))},',
        '...,',
        f'{", ".join(map(repr, dead_canonical_characters[-3:]))}]',
    )
    # Total canonical characters: 876
    # Total dead canonical characters: 60 (6.85%)
    # ['Абсалом', 'Банкина', 'Белл-мере', ..., 'Хоча', 'Цукими', 'Ягуар Д. Саул']
