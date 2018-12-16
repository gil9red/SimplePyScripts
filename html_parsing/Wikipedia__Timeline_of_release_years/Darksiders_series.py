#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Хронология выхода игр


from common import get_parsed_two_column_wikitable


def is_match_func(table) -> bool:
    return 'TIMELINE OF RELEASE YEARS' in table.caption.text.strip().upper()


url = 'https://en.wikipedia.org/wiki/Darksiders_(series)'
for year, name in get_parsed_two_column_wikitable(url, is_match_func):
    print(f'{year}: {name}')
