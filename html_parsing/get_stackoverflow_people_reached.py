#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import Optional
import re

from bs4 import BeautifulSoup
import requests


def get_stackoverflow_people_reached(url: str) -> Optional[str]:
    rs = requests.get(url)
    rs.raise_for_status()

    root = BeautifulSoup(rs.content, 'html.parser')
    return root.find(text=re.compile('^~\d+\.?\d*'))


if __name__ == '__main__':
    url = 'https://ru.stackoverflow.com/users/201445/gil9red'
    print(get_stackoverflow_people_reached(url))
    # ~412k

    url = 'https://ru.stackoverflow.com'
    print(get_stackoverflow_people_reached(url))
    # None

    print()

    urls = [
        'https://ru.stackoverflow.com/users/213987/a-k',
        'https://ru.stackoverflow.com/users/17609/%d0%ae%d1%80%d0%b8%d0%b9%d0%a1%d0%9f%d0%b1',
        'https://ru.stackoverflow.com/users/1984/nofate',
        'https://stackoverflow.com/users/541136/aaron-hall',
        'https://stackoverflow.com/users/106224/boltclock',
        'https://stackoverflow.com/users/168175/flexo',
    ]
    for url in urls:
        print(get_stackoverflow_people_reached(url))
    # ~215k
    # ~750k
    # ~1.4m
    # ~112.5m
    # ~40.5m
    # ~4.7m
