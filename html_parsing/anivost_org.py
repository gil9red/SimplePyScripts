#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re

import requests
from bs4 import BeautifulSoup


def get_last_series(url: str) -> int:
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')

    fields_str = root.select_one('ul.flist').get_text(strip=True)
    if not fields_str:
        raise Exception('Не удалось найти описание полей аниме!')

    m = re.search(r'Добавлена:\s*(\d+)\s*серия', fields_str)
    if not m:
        raise Exception('Не удалось найти номер последней серии!')

    return int(m.group(1))


if __name__ == '__main__':
    url = 'https://anivost.org/24-chernyy-klever.html'
    print(get_last_series(url))
    # 170
