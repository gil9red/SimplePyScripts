#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.parse import urljoin

import requests

# pip install simple-wait
from simple_wait import wait


session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"

session.get("https://tolko-tebe.ru/")


headers = {
    "X-Requested-With": "XMLHttpRequest",
}

while True:
    rs = session.post("https://tolko-tebe.ru/uspeykupit", headers=headers)
    data = rs.json()

    title = data["title"]

    price = data["price"]
    price_action = data["price_action"]

    mins = data["mins"]
    secs = data["secs"]
    time_left = f"{mins}:{secs}"

    url_product = urljoin(rs.url, "/product/" + data["path"])
    print(
        f"{title!r}\n"
        f"    Цена {price} ₽, со скидкой {price_action} ₽\n"
        f"    {url_product}\n"
        f"    Осталось: {time_left}\n"
        # f"    raw_data: {data}\n"
    )

    wait(minutes=mins, seconds=secs)

# OUTPUT example:
# 'SKINLITE Очищающая маска, стягивающая поры'
#     Цена 385 ₽, со скидкой 193 ₽
#     https://tolko-tebe.ru/product/skinlite-ochischayuschaya-maska-styagivayuschaya-pory
#     Осталось: 12:47
