#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from collections import defaultdict

import requests
from bs4 import BeautifulSoup


session = requests.Session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"


rs = session.get("https://isaac-items.ru/")
rs.raise_for_status()

game_by_number: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

soup = BeautifulSoup(rs.content, "html.parser")
for div_group in soup.select(".library-background > div"):
    class_items = div_group.attrs.get("class", [])
    class_str = str(class_items)
    if "-container" not in class_str or "popup-container" in class_str:
        continue

    is_rebirth = "rebirth" in class_items
    is_afterbirth = "afterbirth" in class_items and "plus" not in class_items
    is_afterbirth_plus = "afterbirth" in class_items and "plus" in class_items
    is_repentance = "repentance" in class_items

    if "rebirth" in class_items:
        game_name = "Rebirth"
    elif "afterbirth" in class_items and "plus" not in class_items:
        game_name = "Afterbirth"
    elif "afterbirth" in class_items and "plus" in class_items:
        game_name = "Afterbirth +"
    elif "repentance" in class_items:
        game_name = "Repentance"
    else:
        raise Exception(f"Unknown game by class: {class_items}")

    if "items-" in class_str:
        category_name = "items"
    elif "trinkets-" in class_str:
        category_name = "trinkets"
    elif "tarot-" in class_str:
        category_name = "tarot"
    else:
        raise Exception(f"Unknown category by class: {class_items}")

    game_by_number[game_name][category_name] += len(div_group.select("li"))


print(
    "Total items:",
    sum(
        sum(category_by_number.values())
        for category_by_number in game_by_number.values()
    ),
)
print()

for game, category_by_number in game_by_number.items():
    print(f"{game}:")

    for category, number in category_by_number.items():
        print(f"    {category}: {number}")

    print()
"""
Total items: 1031

Repentance:
    items: 173
    trinkets: 61

Rebirth:
    items: 342
    trinkets: 60
    tarot: 123

Afterbirth:
    items: 95
    trinkets: 29

Afterbirth +:
    items: 110
    trinkets: 38
"""
