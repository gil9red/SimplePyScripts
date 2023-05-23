#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.stackoverflow.com/questions/894302/


import requests
from bs4 import BeautifulSoup


url = "https://cenoteka.rs/proizvodi/mlecni-proizvodi/jogurt?page=3"
rs = requests.get(url)
root = BeautifulSoup(rs.content, "lxml")

for category in root.select("#products > .row.section"):
    category_title = category.select_one(".section-title").get_text(strip=True)
    print(category_title)

    for product in category.select("[data-product-id]"):
        try:
            title = product.select_one(".article-name").get_text(strip=True)
            price_list = [
                price.get_text(strip=True)
                for price in product.select(".article-price")
            ]
            print(f"    {title}: {price_list}")

        except:
            pass

    print()
