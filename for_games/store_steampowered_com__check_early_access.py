#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests


session = requests.Session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"


def is_early_access(app_id_or_url: int | str) -> bool:
    if isinstance(app_id_or_url, str):
        url = app_id_or_url
    else:
        app_id = app_id_or_url
        url = f"https://store.steampowered.com/app/{app_id}/"

    rs = session.get(url)
    rs.raise_for_status()

    return 'id="earlyAccess' in rs.text


if __name__ == "__main__":
    # ULTRAKILL
    print(is_early_access(1229490))
    # True

    print(is_early_access("https://store.steampowered.com/app/1229490/ULTRAKILL/"))
    # True
