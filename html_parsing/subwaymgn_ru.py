#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag


@dataclass
class Product:
    title: str
    price: int


def get_price(card: Tag) -> int:
    price_el = card.select_one(".card__price_color_new")
    if not price_el:
        price_el = card.select_one(".card__price_color")
    return int(price_el.get_text(strip=True))


def parse_card(card: Tag) -> Product:
    title = card.select_one(".card__header").get_text(strip=True)
    price = get_price(card)
    return Product(title, price)


def get_main_products(url: str) -> list[Product]:
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, "html.parser")

    return [parse_card(card) for card in root.select(".main-page__products > .card")]


if __name__ == "__main__":
    for url in ["https://subwaymgn.ru", "https://subwaymgn.ru/rolls.html"]:
        items = get_main_products(url)
        items.sort(key=lambda x: x.price)

        print(url)
        for i, x in enumerate(items, 1):
            print(f"{i:2}. {x}")
        print("\n" + "-" * 100 + "\n")
