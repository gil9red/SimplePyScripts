#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from common import get_html, process_td
html = get_html()

from bs4 import BeautifulSoup
root = BeautifulSoup(html, 'html.parser')

# Таблица "Награды Пиратов Соломенной Шляпы"
table = root.select('.wikitable')[0]

# Список строк исключая строку заголовка
row_list = table.select('tr')[1:]

row = 1

for i in range(0, len(row_list), 2):
    row_1 = row_list[i]
    row_2 = row_list[i + 1]
    print(row, [process_td(td) for td in row_1.select('td')])

    text = process_td(row_2.td)

    for line in text.split('\n'):
        parts = line.split(': ', maxsplit=1)
        print('    {:20}: {}'.format(*parts))

    # import re
    # for reward_num, reward_description in re.findall('([а-яА-ЯёЁ]+ награда): (.+?\.)', text, flags=re.IGNORECASE):
    #     print('    {:20}: {}'.format(reward_num, reward_description))

    row += 1
    print()
