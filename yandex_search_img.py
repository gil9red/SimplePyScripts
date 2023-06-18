#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get_images(text: str) -> list[str]:
    url = "https://yandex.ru/images/search?text=" + text

    rs = requests.get(url)
    root = BeautifulSoup(rs.content, "html.parser")

    return [
        urljoin(rs.url, img["src"])
        for img in root.select("img.serp-item__thumb")
    ]


if __name__ == "__main__":
    text = "Котята"
    urls = get_images(text)
    print(f"Urls ({len(urls)})")
    for i, url in enumerate(urls, 1):
        print(f"{i}. {url}")
