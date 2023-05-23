#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import csv
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get_number(text: str) -> int:
    return int("".join(c for c in text.strip() if c.isdigit()))


first = 1
last = 50
step = 50
result = []


while True:
    url = f"https://www.stoloto.ru/4x20/archive?firstDraw={first}&lastDraw={last}&mode=draw"
    print(f"first={first}, last={last}: {url}")

    rs = requests.get(url)
    root = BeautifulSoup(rs.content, "html.parser")

    rows = root.select(".drawings_data .elem > .main")

    # Если пустое, значит достигли конца
    if not rows:
        break

    # Чтобы был порядок от меньшего к большему
    rows.reverse()

    for row in rows:
        date_time_str = row.select_one(".draw_date").text.strip()
        a = row.select_one(".draw > a")
        abs_url = urljoin(url, a["href"])
        number = get_number(a.text)

        numbers = " ".join(
            x.text.strip() for x in row.select(".numbers .numbers_wrapper b")
        )
        prize = get_number(row.select_one(".prize").text)

        item = [number, date_time_str, numbers, prize, abs_url]
        result.append(item)
        print(item)

    first += step
    last += step

print()
print(len(result), result)

# Наибольшая сумма приза
print(max(result, key=lambda x: x[3]))

# Наименьшая сумма приза
print(min(result, key=lambda x: x[3]))
print()

with open("all_lotto.csv", "w", encoding="utf-8", newline="") as f:
    file = csv.writer(f)
    file.writerows(result)
