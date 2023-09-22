#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

import requests
from bs4 import BeautifulSoup


def get_release_versions() -> list[str]:
    rs = requests.get("https://www.python.org/downloads/")
    rs.raise_for_status()

    soup = BeautifulSoup(rs.content, "html.parser")
    return [
        el.get_text(strip=True)
        for el in soup.find_all(
            attrs={"class": "release-version"},
            text=re.compile(r"\d+\.\d+"),
        )
    ]


if __name__ == '__main__':
    print(get_release_versions())
    # ['3.12', '3.11', '3.10', '3.9', '3.8']
