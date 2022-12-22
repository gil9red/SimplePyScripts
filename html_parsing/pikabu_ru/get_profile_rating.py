#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
from bs4 import BeautifulSoup


session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'


def get_profile_rating(url: str) -> int:
    rs = session.get(url)
    rs.raise_for_status()

    root = BeautifulSoup(rs.content, 'html.parser')
    profile_digital_el = root.select_one('.profile__digital')
    if not profile_digital_el:
        raise Exception('Element ".profile__digital" not found!')

    rating_str = profile_digital_el['aria-label']

    # В рейтинге могут быть не цифровые символы, типа пробелов
    return int(''.join(c for c in rating_str if c.isdigit()))


if __name__ == '__main__':
    url = 'https://pikabu.ru/@user4942077'
    print(get_profile_rating(url))
    # 624

    url = 'https://pikabu.ru/@tibidohtel'
    print(get_profile_rating(url))
    # 104087
