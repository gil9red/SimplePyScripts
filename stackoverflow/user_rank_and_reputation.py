#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


URL = 'https://stackexchange.com/leagues/filter-users/355/AllTime/2015-03-27/?filter=gil9red&sort=reputationchange'

import requests
rs = requests.get(URL)
text = rs.text
# print(text)

import re
match = re.search('>#(.+)</span> all time rank', text)
rank = match.group(1)
print('rank:', rank)

match = re.search('>(.+)</span> all time reputation', text)
reputation = match.group(1).replace(',', '')
print('reputation:', reputation)
