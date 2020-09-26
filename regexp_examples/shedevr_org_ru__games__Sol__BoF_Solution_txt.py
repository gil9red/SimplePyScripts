#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
import requests


rs = requests.get('http://shedevr.org.ru/games/Sol/BoF-Solution.txt')
rs.encoding = 'cp1251'

items = re.findall(r'.+?\.\r\n-------------------\r\n', rs.text)
print('Stages:', len(items))
# print(items)
