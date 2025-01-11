#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


@dataclass
class Meme:
    title: str
    url: str
    url_img: str


def get_memes_words(page: int = 1) -> list[Meme]:
    url = "https://memepedia.ru/category/memes/word/"
    if page > 1:
        url = f"{url}page/{page}/"

    rs = requests.get(url)
    rs.raise_for_status()

    items: list[Meme] = []

    root = BeautifulSoup(rs.content, "html.parser")
    for a in root.select(
        "#post-items .category-word > .post-thumbnail > a[href][title]"
    ):
        url_img = urljoin(rs.url, a.select_one("img[src]")["src"])
        items.append(
            Meme(
                title=a["title"],
                url=a["href"],
                url_img=url_img,
            )
        )

    return items


if __name__ == "__main__":
    memes_words: list[Meme] = get_memes_words()
    print(f"Memes Words page 1 ({len(memes_words)}):")
    for meme in memes_words:
        print(f"  {meme}")

    print()

    memes_words: list[Meme] = get_memes_words(page=2)
    print(f"Memes Words page 2 ({len(memes_words)}):")
    for meme in memes_words:
        print(f"  {meme}")
