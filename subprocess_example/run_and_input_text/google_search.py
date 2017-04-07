#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


key = input('Search: ')
print('Search "{}"'.format(key))

import webbrowser
webbrowser.open_new_tab('https://www.google.ru/search?q=' + key)
