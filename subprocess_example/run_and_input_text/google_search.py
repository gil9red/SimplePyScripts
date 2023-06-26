#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import webbrowser


key = input('Search: ')
print(f'Search "{key}"')

webbrowser.open_new_tab(f'https://www.google.ru/search?q={key}')
