#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from collections import defaultdict

# pip install robobrowser
from robobrowser import RoboBrowser


browser = RoboBrowser(
    user_agent="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    parser="lxml",
)

url = "http://www.duma.gov.ru/structure/deputies/?letter=%D0%92%D1%81%D0%B5&by=name&order=asc"
browser.open(url)
if not browser.response.ok:
    print(browser.response.status_code, browser.response.reason)
    sys.exit()

user_by_factions = defaultdict(list)

total = 0

# Парсинг таблицы депутатов
for i, tr in enumerate(browser.select("#lists_list_elements_35 tr")[1:], 1):
    td_list = tr.select("td")
    user = td_list[1].text
    faction = td_list[2].text

    user_by_factions[faction].append(user)
    total += 1

print(f"Total: {total}")

# Сортировка словаря по количеству человек в партии
for faction, users in sorted(
    user_by_factions.items(), key=lambda x: len(x[1]), reverse=True
):
    print(f"{faction} ({len(users)}):")

    for i, user in enumerate(users, 1):
        print(f"    {i}. {user}")

    print()
