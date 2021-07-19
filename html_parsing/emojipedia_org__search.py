#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import Optional

import requests
from bs4 import BeautifulSoup


session = requests.session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'


def get_emoji(text: str) -> Optional[str]:
    url = 'https://emojipedia.org/search/?q=' + text

    rs = session.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')

    result = root.select_one('.search-results > li > h2 a > .emoji')
    if result:
        return result.get_text(strip=True)


if __name__ == '__main__':
    x = get_emoji('cat')
    print(x)
    assert x == '🐈'

    x = get_emoji('1212121212')
    print(x)
    assert x is None
