#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
from bs4 import BeautifulSoup


rs = requests.get('https://mikafood.ru/')
root = BeautifulSoup(rs.content, 'html.parser')

for x in root.select('.box-menu-content .name > a'):
    print(x.text.strip(), x['href'])
