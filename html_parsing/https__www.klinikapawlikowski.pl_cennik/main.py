#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import csv

import requests
from bs4 import BeautifulSoup as bs


HEADERS = {
    "accept": "*/*",
    "user-agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Ubuntu Chromium/77.0.3865.90 Chrome/77.0.3865.90 Safari/537.36"
    ),
}
BASE_URL = "https://www.klinikapawlikowski.pl/cennik/"


def parser(base_url, headers) -> dict:
    data = dict()

    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code != 200:
        print("ERROR")
        return data

    soup = bs(request.content, "lxml")

    for header in soup.select(".dropdown-list__header"):
        # "Konsultacje", "Dermatologia kliniczna" и т.п.
        header_title = header.select_one(".dropdown-list__header__title").getText(
            strip=True
        )

        data[header_title] = dict()

        for block in soup.select(".dropdown-list__body"):
            # "Dermatolog", "Badanie histopatologiczne", и т.п.
            procedure = block.select_one(
                ".dropdown-list__body__block > .dropdown-list__body__block__title"
            ).getText(strip=True)
            items = []

            for item in block.select(".dropdown-list__body__block__item"):
                title = item.select_one(
                    ".dropdown-list__body__block__item__title"
                ).getText(strip=True)
                price = item.select_one(
                    ".dropdown-list__body__block__item__price"
                ).getText(strip=True)
                items.append((title, price))

            data[header_title][procedure] = items

    return data


def files_writer(data: dict):
    with open("parsed_cennik.csv", "a", encoding="utf-8", newline="") as file:
        a_pen = csv.writer(file)
        a_pen.writerow(["Title", "Title_proedure", "Opisanie_procedur", "Ceny"])

        # "Konsultacje", "Dermatologia kliniczna" и т.п.
        for header, procedures in data.items():
            # "Dermatolog", "Badanie histopatologiczne", и т.п.
            for procedure, items in procedures.items():
                for title, price in items:
                    a_pen.writerow([header, procedure, title, price])


if __name__ == "__main__":
    import json

    data = parser(BASE_URL, HEADERS)

    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    files_writer(data)
