#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.request import urlopen, Request
from urllib.parse import urljoin

from bs4 import BeautifulSoup


USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0'


def get_random_quotes_list():
    url = 'https://bash.im/random'
    quotes = []

    try:
        with urlopen(Request(url, headers={'User-Agent': USER_AGENT})) as f:
            root = BeautifulSoup(f.read(), 'html.parser')

            # Remove comics
            for x in root.select('.quote__strips'):
                x.decompose()

            for quote_el in root.select('.quote'):
                try:
                    href = quote_el.select_one('.quote__header_permalink')['href']
                    url = urljoin(url, href)
                    quote_text = quote_el.select_one('.quote__body').get_text(separator='\n', strip=True)
                    quotes.append((quote_text, url))
                except IndexError:
                    pass

    except Exception as e:
        import traceback
        print(traceback.format_exc())

    return quotes


if __name__ == '__main__':
    print(get_random_quotes_list())
