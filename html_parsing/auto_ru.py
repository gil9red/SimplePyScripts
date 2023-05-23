#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get_price(tag) -> int:
    try:
        # Оставляем только цифры
        value = "".join(c for c in tag.get_text() if c.isdigit())
        return int(value)
    except:
        return 0


session = requests.Session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
session.headers["Accept"] = "*/*"


url = "https://auto.ru/schelkovo/cars/hyundai/used/"

rs = session.get(url)
root = BeautifulSoup(rs.content, "html.parser")

for item in root.select(".ListingItem"):
    title_el = item.select_one(".ListingItemTitle__link[href]")

    title = title_el.get_text(strip=True)
    url = urljoin(rs.url, title_el["href"])

    price_el = item.select_one(".ListingItemPrice__content")
    price = get_price(price_el)

    region_el = item.select_one(".MetroListPlace__regionName")
    city = region_el.get_text() if region_el else "-"

    print(f"{title!r}, {price}, {city!r}")
    print(url)
    print()

"""
'Hyundai Solaris I Рестайлинг', 810000, 'Тейково (180\xa0км от\xa0Щелково)'
https://auto.ru/cars/used/sale/hyundai/solaris/1105856012-839475dc/?geo_id=10765

'Hyundai Tucson IV', 3600000, 'Москва'
https://auto.ru/cars/used/sale/hyundai/tucson/1105942340-1686d5bc/?geo_id=10765

'Hyundai Grand Starex I Рестайлинг', 2385000, 'Москва'
https://auto.ru/cars/used/sale/hyundai/grand_starex/1105479054-60792926/?geo_id=10765

...

'Hyundai Sonata IV (EF) Рестайлинг', 245000, 'Москва'
https://auto.ru/cars/used/sale/hyundai/sonata/1105669699-a55923b6/?geo_id=10765

'Hyundai Elantra III (XD2) Рестайлинг', 289000, 'Москва'
https://auto.ru/cars/used/sale/hyundai/elantra/1105696908-ffede62d/?geo_id=10765
"""
