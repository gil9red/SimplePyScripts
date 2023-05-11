#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Хронология выхода игр *Souls
# SOURCE: https://github.com/gil9red/SimplePyScripts/tree/e0a12b17adde0e0505ab54ae30bbe97f5f2cb038/html_parsing/Wikipedia__Timeline_of_release_years


import requests
from bs4 import BeautifulSoup


def get_parsed_two_column_wikitable(url: str) -> [(str, str)]:
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, "html.parser")

    table = root.select_one(".wikitable")

    items = []

    # Timeline of release years
    for tr in table.select("tr"):
        td_items = tr.select("td")
        if len(td_items) != 2:
            continue

        year = td_items[0].text.strip()
        name = td_items[1].i.text.strip()
        items.append((year, name))

    return items


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Souls_(series)"
    for year, name in get_parsed_two_column_wikitable(url):
        print(year, name)

# 2009 Demon's Souls
# 2011 Dark Souls
# 2014 Dark Souls II
# 2015 Dark Souls II: Scholar of the First Sin
# 2016 Dark Souls III
# 2018 Dark Souls: Remastered
