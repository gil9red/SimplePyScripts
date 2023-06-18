#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт, через сервис http://iknowwhatyoudownload.com получает список торрентов текущего ip,
попавшего в базу сервиса.

"""


import time

import requests
from bs4 import BeautifulSoup


def get_my_torrents(append_torrent_size=False):
    rs = requests.get(
        "http://iknowwhatyoudownload.com/ru/peer/", headers={"User-Agent": "-"}
    )
    root = BeautifulSoup(rs.content, "lxml")

    # Если нужно вместе с названием передавать и размер торрента
    if not append_torrent_size:
        return [item.text.strip() for item in root.select(".torrent_files > a")]

    items = list()

    for row in root.select("table > tbody > tr"):
        name = row.select_one(".name-column").text.strip()
        size = row.select_one(".size-column").text.strip()

        items.append((name, size))

    return items


if __name__ == "__main__":
    while True:
        try:
            items = get_my_torrents()
            print(len(items), items)

            # Every 12 hours
            time.sleep(60 * 60 * 12)

        except Exception as e:
            print("Error:", e)
