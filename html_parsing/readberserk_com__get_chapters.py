#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


@dataclass
class Chapter:
    title: str
    url: str


session = requests.Session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"


def get_chapters() -> list[Chapter]:
    url = "https://readberserk.com/"

    rs = session.get(url)
    rs.raise_for_status()

    soup = BeautifulSoup(rs.content, "html.parser")

    search = "Berserk Chapter"
    items = []
    for tr in soup.select("tr"):
        td_name = tr.select_one(f"td:-soup-contains('{search}')")
        if not td_name:
            continue

        td_link = tr.select_one('a[href *= "chapter"]')
        if not td_link:
            continue

        items.append(
            Chapter(
                title=td_name.get_text(strip=True).replace(search, "").strip(),
                url=urljoin(rs.url, td_link["href"]),
            )
        )

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
    Chapter(title='376', url='https://readberserk.com/chapter/berserk-chapter-376/')
    Chapter(title='375', url='https://readberserk.com/chapter/berserk-chapter-375/')
    Chapter(title='374', url='https://readberserk.com/chapter/berserk-chapter-374/')
    Chapter(title='373', url='https://readberserk.com/chapter/berserk-chapter-373/')
    Chapter(title='372', url='https://readberserk.com/chapter/berserk-chapter-372/')
    ...
    Chapter(title='E0', url='https://readberserk.com/chapter/berserk-chapter-e0/')
    Chapter(title='D0', url='https://readberserk.com/chapter/berserk-chapter-d0/')
    Chapter(title='C0', url='https://readberserk.com/chapter/berserk-chapter-c0/')
    Chapter(title='B0', url='https://readberserk.com/chapter/berserk-chapter-b0/')
    Chapter(title='A0', url='https://readberserk.com/chapter/berserk-chapter-a0/')
    """
