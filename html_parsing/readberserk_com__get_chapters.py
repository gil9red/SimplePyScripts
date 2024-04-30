#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


session = requests.Session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"


def get_chapters() -> list[str]:
    url = "https://readberserk.com/"

    rs = session.get(url)
    rs.raise_for_status()

    soup = BeautifulSoup(rs.content, "html.parser")

    search = "Berserk Chapter"
    items = []
    for el in soup.select("td"):
        text = el.get_text(strip=True)
        if search in text:
            items.append(text.replace(search, "").strip())

    if not items:
        raise Exception("Chapters is not found!")

    return items


if __name__ == "__main__":
    chapters = get_chapters()
    print(f"Chapters ({len(chapters)}):")
    print(*chapters[:5], sep="\n")
    print("...")
    print(*chapters[-5:], sep="\n")
    """
    Chapters (394):
    376
    375
    374
    373
    372
    ...
    E0
    D0
    C0
    B0
    A0
    """
