#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.parse import urljoin

# pip install requests==2.32.2
import requests

# pip install beautifulsoup4==4.15.0
from bs4 import BeautifulSoup

HOST: str = "https://cynicmansion.com"

session = requests.session()
session.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    }
)


def get_comics_url_by_id(comics_id: str | int) -> str:
    return f"{HOST}/{comics_id}/"


def get_comics_info(
    comics_id__or__url: str | int,
) -> tuple[str, str, str]:  # TODO: dataclass
    url_comics: str
    if isinstance(comics_id__or__url, str) and comics_id__or__url.startswith("http"):
        url_comics = comics_id__or__url
    else:
        url_comics = get_comics_url_by_id(comics_id__or__url)

    rs = session.get(url_comics)
    rs.raise_for_status()

    root = BeautifulSoup(rs.content, "html.parser")

    title = root.select_one(".comics_name").text.strip()

    url_image = urljoin(rs.url, root.select_one(".comics_image > img")["src"])

    return url_comics, title, url_image


def get_last_commics_id() -> int:
    rs = session.get(HOST)
    rs.raise_for_status()

    root = BeautifulSoup(rs.content, "html.parser")

    # Example: <a href="/2184/">комментарии (1)</a> -> 2184
    return int(
        root.select_one(
            ".comics_wrap:has(.comics_name) table > tr > td:first-child > a[href]"
        )["href"].replace("/", "")
    )


def get_comics_image_url(comics_id__or__url: str | int) -> str:
    _, _, url_image = get_comics_info(comics_id__or__url)
    return url_image


if __name__ == "__main__":
    last_commics_id = get_last_commics_id()
    print("last_commics_id:", last_commics_id)

    print()
    comics_id = 1538
    print(f"About #{comics_id} comics")

    url = get_comics_url_by_id(comics_id)
    print(comics_id, url)
    print()
    print(get_comics_info(comics_id))
    print(get_comics_info(url))
    print()
    print(get_comics_image_url(comics_id))
    print(get_comics_image_url(url))
