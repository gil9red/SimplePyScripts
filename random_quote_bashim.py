#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_random_quotes_list():
    quotes = []

    import requests
    rs = requests.get('http://bash.im/random')

    from lxml import etree
    root = etree.HTML(rs.content)

    for quote_el in root.xpath('//*[@class="quote"]'):
        try:
            text_el = quote_el.xpath('*[@class="text"]')[0]
            quote_text = '\n'.join(text.encode('ISO8859-1').decode('cp1251') for text in text_el.itertext()).strip()

            quotes.append(quote_text)

        except IndexError:
            pass

    return quotes


if __name__ == '__main__':
    print(get_random_quotes_list())
