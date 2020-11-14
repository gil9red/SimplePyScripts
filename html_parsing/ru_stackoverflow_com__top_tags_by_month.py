#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from collections import Counter

import requests
from bs4 import BeautifulSoup


rs = requests.get('https://ru.stackoverflow.com/?tab=month')
root = BeautifulSoup(rs.content, 'html.parser')

tags = []
for summary in root.select('#question-mini-list .question-summary'):
    # First tag: "html css вёрстка svg svg-animation" -> "html"
    tags.append(summary.select_one('.post-tag').text)

print(f'Total: {len(tags)}')
for tag, number in sorted(Counter(tags).items(), key=lambda x: x[1], reverse=True):
    print(f'    {tag}: {number}')

# Total: 47
#     python: 23
#     c++: 9
#     javascript: 5
#     html: 4
#     c#: 1
#     алгоритм: 1
#     любой-язык: 1
#     математика: 1
#     linux: 1
#     css3: 1
