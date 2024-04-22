#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


URL = "https://websniffer.com/"

session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0"


def get_redirected_url(url_from: str) -> str | None:
    rs = session.get(URL, params=dict(url=url_from))
    rs.raise_for_status()

    soup = BeautifulSoup(rs.content, "html.parser")

    data = {
        "url": url_from,
        "antispam": soup.select_one("#antispam")["value"],
        "type": "HEAD",
        "http": "1.1",
        "uak": "0",
    }

    rs = session.post(URL, params=dict(url=url_from), data=data)
    rs.raise_for_status()

    soup = BeautifulSoup(rs.content, "html.parser")
    for tr in soup.select("tr"):
        td_list = tr.select("td")
        if len(td_list) != 2:
            continue

        if "Location:" in str(td_list[0]):
            location = td_list[1].get_text(strip=True)
            return urljoin(url_from, location)


if __name__ == "__main__":
    url_from = "http://ya.ru/"
    print(get_redirected_url(url_from))
    # https://ya.ru/
