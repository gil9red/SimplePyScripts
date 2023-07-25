#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"


def get_number_of_anime_episodes() -> int:
    url = "https://en.wikipedia.org/wiki/Redo_of_Healer"

    rs = session.get(url)
    rs.raise_for_status()

    root = BeautifulSoup(rs.content, "html.parser")

    # Для определения изменения верстки
    # Например, отсутствие эпизодов или появление больше чем 1 элемент с эпизодом
    episodes = []

    for tr in root.select(".infobox tr:has(th.infobox-label)"):
        label = tr.select_one(".infobox-label").text
        if label != "Episodes":
            continue

        data = tr.select_one(".infobox-data").text
        data = "".join(c for c in data if c.isdigit())
        number = int(data)

        episodes.append(number)

    if not episodes:
        raise Exception("Поля с эпизодом не найдены!")

    if len(episodes) > 1:
        raise Exception(f"Полей с эпизодом больше одного: {episodes}!")

    return episodes[0]


if __name__ == "__main__":
    number = get_number_of_anime_episodes()
    print(number)
    # 12
