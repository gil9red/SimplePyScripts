#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_game_list():
    from urllib.parse import urljoin

    import requests
    rs = requests.get('https://games.mail.ru/pc/games/future_hits/')

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'lxml')

    items = []

    # Перебор табличек с играми
    for item in root.select('.b-pc__entities-item'):
        a = item.select_one('.b-pc__entities-title > a')
        title = a.text.strip()

        url = urljoin(rs.url, a['href'])

        description = item.select_one('.b-pc__entities-descr').text.strip()
        img_url = item.select_one('.b-pc__entities-img')['src']
        release_date = item.select_one('.b-pc__entities-author').text.strip()

        items.append((title, description, release_date, url, img_url))

    return items


if __name__ == '__main__':
    game_list = get_game_list()

    # # Full
    # for i, (title, description, release_date, url, img_url) in enumerate(game_list, 1):
    #     print('{:2}. "{}" ({}): {} [{}]\n{}\n'.format(i, title, release_date, url, img_url, description))

    # # First 5
    # for i, (title, description, release_date, url, img_url) in enumerate(game_list[:5], 1):
    #     print('{:2}. "{}" ({}): {} [{}]\n{}\n'.format(i, title, release_date, url, img_url, description))

    # # Sorted by title
    # for i, (title, description, release_date, url, img_url) in enumerate(sorted(game_list, key=lambda x: x[0]), 1):
    #     print('{:2}. "{}" ({}): {} [{}]\n{}\n'.format(i, title, release_date, url, img_url, description))

    # Sorted by year
    import re
    get_year = lambda text: int(re.search('\d{4}', text).group())
    game_list = sorted(game_list, key=lambda x: get_year(x[2]))

    for i, (title, description, release_date, url, img_url) in enumerate(game_list, 1):
        print('{:2}. "{}" ({}): {} [{}]\n{}\n'.format(i, title, release_date, url, img_url, description))
