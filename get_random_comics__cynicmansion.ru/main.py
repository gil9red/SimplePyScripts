#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get_comics_url_by_id(comics_id: str | int) -> str:
    return f"https://cynicmansion.ru/{comics_id}/"


def get_comics_info(
    comics_id__or__url: str | int,
) -> tuple[str, str, str]:
    if type(comics_id__or__url) == str and comics_id__or__url.startswith("http"):
        url_comics = comics_id__or__url
    else:
        url_comics = get_comics_url_by_id(comics_id__or__url)

    rs = requests.get(url_comics)
    root = BeautifulSoup(rs.content, "lxml")

    title = root.select_one(".comics_name").text.strip()

    url_image = urljoin(rs.url, root.select_one(".comics_image > img")["src"])

    return url_comics, title, url_image


def get_random_comics_url() -> str:
    url = "https://cynicmansion.ru/"

    rs = requests.get(url)
    root = BeautifulSoup(rs.content, "lxml")
    comics_number = int(
        root.select_one(".comics_wrap > table > tr > td > a")["href"].replace("/", "")
    )

    random_comics_number = random.randint(1, comics_number)
    return get_comics_url_by_id(random_comics_number)


def get_comics_image_url(comics_id__or__url: str | int) -> str:
    _, _, url_image = get_comics_info(comics_id__or__url)
    return url_image


def get_random_comics_image_url() -> str:
    url = get_random_comics_url()

    return get_comics_image_url(url)


def get_random_comics_info() -> tuple[str, str, str]:
    url = get_random_comics_url()

    return get_comics_info(url)


if __name__ == "__main__":
    url_comics = get_random_comics_url()
    print("url_comics:", url_comics)

    url_image = get_comics_image_url(url_comics)
    print("url_image:", url_image)

    comics_id = url_comics.split("/")[-2]

    file_name = f"{comics_id}.png"
    print("Save in:", file_name)

    with open(file_name, mode="wb") as f:
        rs = requests.get(url_image)
        f.write(rs.content)

    print()
    print("Random comics image:")
    print(get_random_comics_image_url())
    print(get_random_comics_image_url())
    print(get_random_comics_image_url())

    print()
    print("Random comics image:")
    print(get_random_comics_info())
    print(get_random_comics_info())
    print(get_random_comics_info())

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
