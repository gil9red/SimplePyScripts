#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get_game_list():
    rs = requests.get("https://games.mail.ru/pc/games/future_hits/")
    root = BeautifulSoup(rs.content, "lxml")

    items = []

    # Перебор табличек с играми
    for item in root.select(".b-pc__entities-item"):
        a = item.select_one(".b-pc__entities-title > a")
        title = a.text.strip()

        url = urljoin(rs.url, a["href"])

        description = item.select_one(".b-pc__entities-descr").text.strip()
        img_url = item.select_one(".b-pc__entities-img")["src"]
        release_date = item.select_one(".b-pc__entities-author").text.strip()

        items.append((title, description, release_date, url, img_url))

    return items


if __name__ == "__main__":
    game_list = get_game_list()

    def print_list(items):
        for i, (title, description, release_date, url, img_url) in enumerate(items, 1):
            print(
                f'{i:2}. "{title}" ({release_date}): {url} [{img_url}]\n{description}\n'
            )

    # Full
    print_list(game_list)

    # # First 5
    # new_game_list = game_list[:5]
    # print_list(new_game_list)
    #
    # # Sorted by title
    # new_game_list = sorted(game_list, key=lambda x: x[0])
    # print_list(new_game_list)

    # # Sorted by year, reverse
    # import re
    # get_year = lambda text: int(re.search('\d{4}', text).group())
    # new_game_list = sorted(game_list, key=lambda x: get_year(x[2]), reverse=True)
    # print_list(new_game_list)
