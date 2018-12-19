#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'



from bs4 import BeautifulSoup
root = BeautifulSoup(open('3.html', encoding='utf-8'), 'html.parser')

table = root.select_one('table')

for tr in table.select('tr'):
    tds = tr.select('td')
    if len(tds) != 3:
        continue

    title_node, description_node = tds[1:]

    title = title_node.text.strip()
    description = description_node.text.strip()

    print('{:20}: {}'.format(title, repr(description)))
