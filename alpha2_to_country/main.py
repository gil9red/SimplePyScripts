#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/f2c11477ae4410e5a9d47272b72cb69354c271b8/html_parsing/ru_wikipedia_org__wiki__ISO_3166_1.py


import json
from pathlib import Path

from bs4 import BeautifulSoup
import requests


FILE_NAME_COUNTRY = Path(__file__).resolve().parent / 'alpha2_to_country.json'
ALPHA2_TO_COUNTRY = None


def init():
    global ALPHA2_TO_COUNTRY

    if FILE_NAME_COUNTRY.exists():
        ALPHA2_TO_COUNTRY = json.loads(
            FILE_NAME_COUNTRY.read_text('utf-8')
        )
        return

    rs = requests.get('https://ru.wikipedia.org/wiki/ISO_3166-1')
    root = BeautifulSoup(rs.content, 'html.parser')

    ALPHA2_TO_COUNTRY = dict()

    for tr in root.select_one('.wikitable').select('tr'):
        td_list = tr.select('td')
        if not td_list:
            continue

        td_country, td_alpha2, td_alpha3, td_num_code, _ = td_list
        country = td_country.get_text(strip=True)
        alpha2 = td_alpha2.get_text(strip=True)

        ALPHA2_TO_COUNTRY[alpha2] = country

    json.dump(
        ALPHA2_TO_COUNTRY,
        open(FILE_NAME_COUNTRY, 'w', encoding='utf-8'),
        ensure_ascii=False,
        indent=4
    )


init()


def get_country(alpha2: str) -> str:
    return ALPHA2_TO_COUNTRY[alpha2]


if __name__ == '__main__':
    print(get_country('RU'))
    # Россия

    print(get_country('US'))
    # США

    print(get_country('DE'))
    # Германия
