#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


URL = "https://www.viva64.com/ru/customers/"

session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"


def get_customers() -> list[str]:
    rs = session.get(URL)
    root = BeautifulSoup(rs.content, "html.parser")

    return [a["href"] for a in root.select("#tab-all a[href]")]


if __name__ == "__main__":
    items = get_customers()
    print(len(items))
    # 228
