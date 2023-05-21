#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


def get_exclusive_games() -> list:
    URL = "https://www.listal.com/list/psp-exclusives"
    URL_MORE_ITEMS = "https://www.listal.com/item-list/"

    def _get_games(el) -> list:
        return [a.get_text(strip=True) for a in el.select(".titletitle > a")]

    session = requests.session()
    session.headers[
        "User-Agent"
    ] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"

    rs = session.get(URL)
    root = BeautifulSoup(rs.content, "html.parser")

    custom_list_items = root.select_one("#customlistitems")
    list_id = custom_list_items["data-listid"]
    step = int(custom_list_items.select_one(".listtotals > .end").text)
    max_items = int(custom_list_items.select_one(".listtotals > .itemtotal").text)

    exclusive_games = _get_games(custom_list_items)

    for offset in range(step, max_items, step):
        params = {
            "listid": list_id,
            "offset": offset,
            "defaultsortby": "",
            "filter[rating]": "",
            "filter[listtype]": "",
        }
        headers = {
            "X-Requested-With": "XMLHttpRequest",
        }
        rs = session.post(URL_MORE_ITEMS, data=params, headers=headers)
        items_html = rs.json()["items"]
        root = BeautifulSoup(items_html, "html.parser")
        exclusive_games += _get_games(root)

    return exclusive_games


if __name__ == "__main__":
    exclusive_games = get_exclusive_games()

    print(f"Games ({len(exclusive_games)}):")
    for i, game in enumerate(exclusive_games, 1):
        print(f"  {i:3}. {game}")

    # Games (148):
    #     1. 300: March To Glory
    #     2. The 3rd Birthday
    #     3. ATV Offroad Fury: Blazin' Trails
    #     4. ATV Offroad Fury Pro
    #     5. Ace Combat X: Skies of Deception
    #   ...
    #   146. WTF: Work Time Fun
    #   147. Yu-Gi-Oh! Gx Tag Force 2
    #   148. Yu-Gi-Oh! GX: Tag Force
