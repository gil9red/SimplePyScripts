#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json
import time
from typing import Dict
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests


def parse() -> Dict[str, int]:
    url = 'http://rik-i-morti.ru/'

    s = requests.session()
    rs = s.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')

    season_by_series_num = dict()

    for cell in root.select_one('.alltable').select('.cell'):
        title = cell.p.get_text(strip=True)
        season_url = urljoin(rs.url, cell.a['href'])

        rs_season = s.get(season_url)
        root = BeautifulSoup(rs_season.content, 'html.parser')
        season_by_series_num[title] = len(root.select('#dle-content > .short-item'))

        # Не нужно напрягать сайт
        time.sleep(1)

    return season_by_series_num


if __name__ == '__main__':
    season_by_series_num = parse()
    print('Total seasons:', len(season_by_series_num))
    print('Total episodes:', sum(season_by_series_num.values()))
    # Total seasons: 4
    # Total episodes: 41
