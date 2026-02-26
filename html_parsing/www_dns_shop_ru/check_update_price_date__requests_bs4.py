#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import os

from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def go() -> None:
    url = "http://www.dns-shop.ru/"

    rs = requests.get(url)
    root = BeautifulSoup(rs.content, "html.parser")

    for a in root.select("#price-list-downloader a"):
        href = a["href"]

        # Нужен вариант только с .xls (также там есть вариант с .zip)
        if not href.endswith(".xls"):
            continue

        file_url = urljoin(url, href)

        update_date_text = a.next_sibling.strip()

        match = re.search(r"\d{,2}.\d{,2}.\d{4}", update_date_text)
        if not match:
            continue

        date_string = match.group()

        file_name = os.path.basename(href)
        file_name = date_string + "_" + file_name

        print(datetime.today().date(), file_name, file_url)


if __name__ == "__main__":
    import time

    while True:
        go()

        # Настроим вызов загрузки страницы на каждые 10 часов
        time.sleep(60 * 60 * 10)
