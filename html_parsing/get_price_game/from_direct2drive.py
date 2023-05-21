#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests


text = "titan"
url = "https://www.direct2drive.com/backend/api/productquery/findpage?search.keywords={text}"

rs = requests.get(url)
print(rs)

data = rs.json()
print(data)

for game in data["products"]["items"]:
    offer = game["offerActions"][0]
    print(
        game["title"],
        offer["purchasePrice"]["amount"]
        + " "
        + offer["purchasePrice"]["currency"]["isoCode"],
    )
