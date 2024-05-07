#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get_gist_file(gist_url: str, file_name: str) -> str:
    rs = requests.get(gist_url)
    soup = BeautifulSoup(rs.content, "html.parser")

    a_all = soup.find("a", {"href": re.compile(rf"/raw/.+/{re.escape(file_name)}")})
    if not a_all:
        raise Exception(f"Не удалось найти файл {file_name!r} в {gist_url!r}")

    url_all = urljoin(rs.url, a_all["href"])

    rs = requests.get(url_all)
    rs.raise_for_status()

    return rs.text
