#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_books():
    import requests
    rs = requests.get('http://vitaly-zykov.ru/knigi')

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'lxml')

    return [x.text.strip().replace('"', '') for x in root.select('.book_tpl > h3')]


if __name__ == '__main__':
    for i, book in enumerate(get_books(), 1):
        print('{:>2}. {}'.format(i, book))
