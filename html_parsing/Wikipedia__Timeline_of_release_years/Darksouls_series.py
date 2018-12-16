#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Хронология выхода игр


from common import get_parsed_two_column_wikitable


url = 'https://en.wikipedia.org/wiki/Souls_(series)'
for year, name in get_parsed_two_column_wikitable(url):
    print(year, name)
