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
    profile_avatar_el = root.select_one('#user-card .profile-avatar')
    if not profile_avatar_el:
        return

    text = profile_avatar_el.get_text(strip=True, separator='\n')
    m = re.search(r'(\d+\.?\d*[km]?)\s*(затронуто|reached)', text)
    if not m:
        raise Exception('Reached not found!')

    return m.group(1)


if __name__ == '__main__':
    url = 'https://ru.stackoverflow.com/users/201445/gil9red'
    print(get_stackoverflow_people_reached(url))
    # 1.4m

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
    """
    513k
    1.1m
    1.7m
    148.1m
    50.3m
    5.5m
    """
