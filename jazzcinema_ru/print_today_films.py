#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin
from urllib.request import urlopen

from bs4 import BeautifulSoup


if __name__ == '__main__':
    url = 'http://www.jazzcinema.ru/'

    with urlopen(url) as f:
        root = BeautifulSoup(f.read())

        # Получение фильмов в текущей вкладке (по идеи, текущая вкладка -- текущий день)
        for border in root.select('.schedule.active .border'):
            a = border.select_one('.movie .title > a')
            url = urljoin(url, a['href'])
            print(a['title'], url)
            print('   ', border.select_one('.genre').text)

            for seanse in border.select('.seanses'):
                time = seanse.select_one('a').text
                price = seanse.select_one('.price').text
                print('    {} : {}'.format(time, price))

            print()
