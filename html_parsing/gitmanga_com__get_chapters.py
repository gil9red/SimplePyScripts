#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"


@dataclass
class Chapter:
    title: str
    url: str


def get_chapters(url: str) -> list[Chapter]:
    rs = session.get(url)
    rs.raise_for_status()

    soup = BeautifulSoup(rs.content, "html.parser")
    return [
        Chapter(
            title=el.select_one(".item-title").get_text(strip=True),
            url=urljoin(rs.url, el.a["href"]),
        )
        for el in soup.select(".chapters-list__item")
    ]


if __name__ == "__main__":

    def print_chapter(items: list[Chapter]):
        print(f"Chapters ({len(items)}):")
        print(f"    {items[0]}")
        print("    ...")
        print(f"    {items[-1]}")

    url = "https://gitmanga.com/764-berserk.html"
    items = get_chapters(url)
    print_chapter(items)
    """
    Chapters (387):
        Chapter(title='Том 1. Глава 0 - Berserk - The Prototype', url='https://gitmanga.com/read-764-berserk.html?t=1&g=0&p=1')
        ...
        Chapter(title='Том 42. Глава 371 - Угасающий свет в гнетущей тёмной ночи', url='https://gitmanga.com/read-764-berserk.html?t=42&g=371&p=1')
    """

    print()

    url = "https://gitmanga.com/605-igrok.html"
    items = get_chapters(url)
    print_chapter(items)
    """
    Chapters (447):
        Chapter(title='Том 1. Глава 1', url='https://gitmanga.com/read-605-igrok.html?t=1&g=1&p=1')
        ...
        Chapter(title='Том 6. Глава 15', url='https://gitmanga.com/read-605-igrok.html?t=6&g=15&p=1')
    """
