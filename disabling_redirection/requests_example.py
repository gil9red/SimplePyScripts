#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests


rs = requests.get('http://ya.ru/')
print(rs.status_code, rs.url)
# 200 https://ya.ru/

rs = requests.get('http://ya.ru/', allow_redirects=False)
print(rs.status_code, rs.url)
# 302 http://ya.ru/
