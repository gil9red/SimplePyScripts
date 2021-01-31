#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests


rs = requests.get('http://ya.ru/')
print(rs)      # <Response [200]>
print(rs.url)  # https://ya.ru/ - автоматически перенаправлено на https

print()

rs = requests.get('http://ya.ru/', allow_redirects=False)
print(rs)      # <Response [302]>
print(rs.url)  # http://ya.ru/
