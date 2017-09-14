#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
rs = requests.get('https://horo.mail.ru/prediction/pisces/today/')

from bs4 import BeautifulSoup
root = BeautifulSoup(rs.content, 'lxml')
text = root.select_one('.article__text').text.strip()
print(repr(text))
print(text)
