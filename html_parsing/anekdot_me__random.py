#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import Tuple

import requests
from bs4 import BeautifulSoup


URL = 'https://anekdot.me/wiki/Служебная:RandomInCategory/Анекдоты'


def get_random() -> Tuple[int, str]:
    rs = requests.get(URL)
    root = BeautifulSoup(rs.content, 'html.parser')

    anekdot_id = int(rs.url.split('/')[-1])
    text = root.select_one('.anekdot-centred-text').get_text(strip=True)

    return anekdot_id, text


if __name__ == '__main__':
    anekdot_id, text = get_random()
    print(f'#{anekdot_id}:')
    print(text)
    # #5745:
    # Американский военный отряд.
    # — Капитан, мы уже 5 дней бродим по этой чёртовой Камбодже и до сих пор не видели ни одного МакДональдса!
    # — Джон, ты дурак! Это же джунгли — здесь везде можно!
