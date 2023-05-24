#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


start = 0

# TODO: Watch rs.json()['total_count']
i = 0
while i < 5:
    i += 1

    url = f"https://steamcommunity.com/market/search/render/?query=&start={start}&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=730"
    rs = requests.get(url)

    html = rs.json()["results_html"]
    root = BeautifulSoup(html, "html.parser")

    for a in root.select(".market_listing_row_link"):
        print(a["href"])

    print("\n" + "-" * 100 + "\n")

    start += 10

# https://steamcommunity.com/market/listings/730/Glove%20Case
# https://steamcommunity.com/market/listings/730/Clutch%20Case
# https://steamcommunity.com/market/listings/730/Operation%20Breakout%20Weapon%20Case
# https://steamcommunity.com/market/listings/730/Prisma%202%20Case
# https://steamcommunity.com/market/listings/730/Gamma%202%20Case
# https://steamcommunity.com/market/listings/730/Operation%20Phoenix%20Weapon%20Case
# https://steamcommunity.com/market/listings/730/Shattered%20Web%20Case
# https://steamcommunity.com/market/listings/730/MP9%20%7C%20Orange%20Peel%20%28Field-Tested%29
# https://steamcommunity.com/market/listings/730/Spectrum%20Case
# https://steamcommunity.com/market/listings/730/Prisma%20Case
#
# ----------------------------------------------------------------------------------------------------
#
# https://steamcommunity.com/market/listings/730/Chroma%202%20Case
# https://steamcommunity.com/market/listings/730/Spectrum%202%20Case
# https://steamcommunity.com/market/listings/730/Five-SeveN%20%7C%20Coolant%20%28Field-Tested%29
# https://steamcommunity.com/market/listings/730/Gamma%20Case
# https://steamcommunity.com/market/listings/730/M4A1-S%20%7C%20Decimator%20%28Field-Tested%29
# https://steamcommunity.com/market/listings/730/Danger%20Zone%20Case
# https://steamcommunity.com/market/listings/730/Desert%20Eagle%20%7C%20Mecha%20Industries%20%28Minimal%20Wear%29
# https://steamcommunity.com/market/listings/730/SSG%2008%20%7C%20Dragonfire%20%28Field-Tested%29
# https://steamcommunity.com/market/listings/730/Berlin%202019%20Minor%20Challengers%20Autograph%20Capsule
# https://steamcommunity.com/market/listings/730/CS20%20Case
#
# ...
#
