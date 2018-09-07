#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import typing


def get_books() -> typing.List[str]:
    import requests
    rs = requests.get('http://vitaly-zykov.ru/knigi')

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'html.parser')

    return [x.text.strip().replace('"', '') for x in root.select('.book_tpl > h3')]


if __name__ == '__main__':
    books = get_books()
    print('Items ({}): {}'.format(len(books), books))
