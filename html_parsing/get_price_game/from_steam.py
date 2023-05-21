#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

import requests
from bs4 import BeautifulSoup


def search_game_price_list(name: str) -> list:
    # category1 = 998 (Game)
    url = f"https://store.steampowered.com/search/?category1=998&os=win&supportedlang=english&term={name}"

    game_price_list = []

    rs = requests.get(url)
    if not rs.ok:
        print(f"Что-то пошло не так: {rs.status_code}\n{rs.text}")
        return game_price_list

    root = BeautifulSoup(rs.content, "html.parser")

    for div in root.select(".search_result_row"):
        name = div.select_one(".title").text.strip()

        # Ищем тег скидки
        if div.select_one(".search_discount > span"):
            price = div.select_one(".search_price > span > strike").text.strip()
        else:
            price = div.select_one(".search_price").text.strip()

        # Если цены нет (например, игра еще не продается)
        if not price:
            price = None
        else:
            # Если в цене нет цифры считаем что это "Free To Play" или что-то подобное
            match = re.search(r"\d", price)
            if not match:
                price = 0

        game_price_list.append((name, price))

    return game_price_list


if __name__ == "__main__":
    text = "resident evil 6"
    game_price_list = search_game_price_list(text)
    for name, price in game_price_list:
        print(name, price, sep=" / ")

    print()
    text = "prey"
    game_price_list = search_game_price_list(text)
    for name, price in game_price_list:
        print(name, price, sep=" / ")
