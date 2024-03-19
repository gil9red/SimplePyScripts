#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


@dataclass
class Video:
    title: str
    url: str


session = requests.Session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"


def get_all_series() -> list[Video]:
    rs = session.get("https://theboys.fun/")
    rs.raise_for_status()

    soup = BeautifulSoup(rs.content, "html.parser")

    items: list[Video] = []
    for el in soup.select(".seasons .season_sir"):
        if not el.select_one(".release_on"):
            continue

        title_el = el.select_one(".season_sir_t")
        items.append(
            Video(
                title=title_el.get_text(strip=True),
                url=title_el.a["href"],
            )
        )

    items.sort(key=lambda video: int("".join(c for c in video.title if c.isdigit())))

    return items


if __name__ == "__main__":
    items = get_all_series()
    print(f"Video {len(items)}:")
    for video in items:
        print(f"    {video.title!r}: {video.url}")
    """
    Video 24:
        'Сезон 1 серия 1': https://theboys.fun/1-pacany-1-sezon-1-serija1.html
        'Сезон 1 серия 2': https://theboys.fun/2-pacany-1-sezon-2-serija.html
        'Сезон 1 серия 3': https://theboys.fun/3-pacany-1-sezon-3-serija1.html
        'Сезон 1 серия 4': https://theboys.fun/4-pacany-1-sezon-4-serija.html
        'Сезон 1 серия 5': https://theboys.fun/5-pacany-1-sezon-5-serija.html
        'Сезон 1 серия 6': https://theboys.fun/6-pacany-1-sezon-6-serija.html
        'Сезон 1 серия 7': https://theboys.fun/7-pacany-1-sezon-7-serija.html
        'Сезон 1 серия 8': https://theboys.fun/8-pacany-1-sezon-8-serija.html
        'Сезон 2 серия 1': https://theboys.fun/9-pacany-2-sezon-1-serija.html
        'Сезон 2 серия 2': https://theboys.fun/10-pacany-2-sezon-2-serija.html
        'Сезон 2 серия 3': https://theboys.fun/11-pacany-2-sezon-3-serija.html
        'Сезон 2 серия 4': https://theboys.fun/12-pacany-2-sezon-4-serija.html
        'Сезон 2 серия 5': https://theboys.fun/13-pacany-2-sezon-5-serija.html
        'Сезон 2 серия 6': https://theboys.fun/14-pacany-2-sezon-6-serija.html
        'Сезон 2 серия 7': https://theboys.fun/15-pacany-2-sezon-7-serija.html
        'Сезон 2 серия 8': https://theboys.fun/16-pacany-2-sezon-8-serija.html
        'Сезон 3 серия 1': https://theboys.fun/51-pacany-3-sezon-1-serija21.html
        'Сезон 3 серия 2': https://theboys.fun/52-pacany-3-sezon-2-serija21.html
        'Сезон 3 серия 3': https://theboys.fun/53-pacany-3-sezon-3-serija20.html
        'Сезон 3 серия 4': https://theboys.fun/54-pacany-3-sezon-4-serija16.html
        'Сезон 3 серия 5': https://theboys.fun/55-pacany-3-sezon-5-serija13.html
        'Сезон 3 серия 6': https://theboys.fun/56-pacany-3-sezon-6-serija8.html
        'Сезон 3 серия 7': https://theboys.fun/57-pacany-3-sezon-7-serija6.html
        'Сезон 3 серия 8': https://theboys.fun/58-pacany-3-sezon-8-serija3.html
    """
