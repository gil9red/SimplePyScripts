#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from typing import Any
from urllib.parse import urlparse

import requests


HOST_API: str = "https://api.cdnlibs.org"

session = requests.Session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0"


def get_chapters(url: str) -> list[str]:
    result = urlparse(url)
    host: str = f"{result.scheme}://{result.netloc}"
    slug: str = result.path.rstrip("/").split("/")[-1]

    url_api: str = f"{HOST_API}/api/manga/{slug}/chapters"

    headers = {
        "Referer": host,
        "Content-Type": "application/json",
        "Origin": host,
    }
    rs = session.get(url_api, headers=headers)
    rs.raise_for_status()

    data: list[dict[str, Any]] = rs.json()["data"]

    items: list[str] = []
    for item in data:
        volume = item["volume"]
        number = item["number"]
        name = item["name"]

        chapter_name: str = f"Том {volume} Глава {number}"
        if name:
            chapter_name = f"{chapter_name} - {name}"

        items.append(chapter_name)

    return items


if __name__ == "__main__":
    import time

    for url in [
        "https://mangalib.me/ru/manga/12123--mieru-ko-chan",
        "https://mangalib.me/ru/manga/206--one-piece?from=catalog",
    ]:
        print(url)

        chapters: list[str] = get_chapters(url)
        print(f"Chapters ({len(chapters)}):")
        print(*chapters[:5], sep="\n")
        print("...")
        print(*chapters[-5:], sep="\n")
        print()

        time.sleep(1)
    """
    https://mangalib.me/ru/manga/12123--mieru-ko-chan
    Chapters (80):
    Том 1 Глава 1
    Том 1 Глава 2
    Том 1 Глава 3
    Том 1 Глава 4
    Том 1 Глава 5
    ...
    Том 13 Глава 65
    Том 13 Глава 66
    Том 13 Глава 67
    Том 13 Глава 68
    Том 14 Глава 69
    
    https://mangalib.me/ru/manga/206--one-piece?from=catalog
    Chapters (1184):
    Том 1 Глава 0 - Рассвет романтики
    Том 1 Глава 0.5 - Strong World
    Том 1 Глава 1 - На заре приключений
    Том 1 Глава 2 - Луффи Соломенная шляпа
    Том 1 Глава 3 - Первая встреча: Охотник на пиратов Зоро
    ...
    Том 108 Глава 1174 - Сильнейшее чувство в мире
    Том 108 Глава 1175 - Нидхегг
    Том 108 Глава 1176 - С гордостью
    Том 108 Глава 1177 - Гнев
    Том 108 Глава 1178 - Кошмар закончился
    """
