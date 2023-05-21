#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import requests


text = "titan quest"
url = (
    "https://www.gog.com/games/ajax/filtered?language=en&mediaType=game&page=1&sort=bestselling"
    f"&system=windows_10,windows_7,windows_8,windows_vista,windows_xp&search={text}"
)

rs = requests.get(url)
print(rs)

data = rs.json()
print(data)

if not data["totalGamesFound"]:
    print("Not found game")
    sys.exit()

for game in data["products"]:
    print(game["title"], game["price"]["amount"] + game["price"]["symbol"])
