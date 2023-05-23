#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from bs4 import BeautifulSoup

from common import get_html, process_td


html = get_html()

root = BeautifulSoup(html, "html.parser")

# Таблица "Награды Пиратов Соломенной Шляпы"
table = root.select(".wikitable")[0]

# Список строк исключая строку заголовка
row_list = table.select("tr")[1:]

row = 1
for i in range(0, len(row_list), 2):
    row_1 = row_list[i]
    row_2 = row_list[i + 1]
    print(row, [process_td(td) for td in row_1.select("td")])

    text = process_td(row_2.td)

    for line in text.split("\n"):
        parts = line.split(": ", maxsplit=1)
        print("    {:20}: {}".format(*parts))

    row += 1
    print()
