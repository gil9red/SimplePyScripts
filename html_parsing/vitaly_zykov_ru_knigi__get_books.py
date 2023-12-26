#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


def get_books() -> list[str]:
    rs = requests.get("http://vitaly-zykov.ru/knigi")
    root = BeautifulSoup(rs.content, "html.parser")

    return [
        x.get_text(strip=True).replace('"', "")
        for x in root.select(".book_tpl > h3")
    ]


if __name__ == "__main__":
    books = get_books()
    print(f"Items ({len(books)}): {books}")
