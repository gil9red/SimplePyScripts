#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import os

from urllib.parse import urljoin

import requests


def get_html_by_url__from_cache(url, cache_dir="cache"):
    os.makedirs(cache_dir, exist_ok=True)

    file_name = os.path.basename(url)
    file_name = re.sub(r"[^a-zA-Z\d]", "_", file_name)
    file_name = cache_dir + "/" + file_name + ".html"

    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return f.read()

    with open(file_name, "wb") as f:
        rs = requests.get(url)
        f.write(rs.content)

        return rs.content


def parse_item(url, node_item) -> dict:
    data = {
        "name": node_item.select_one(".link").text.strip(),
        "url": urljoin(url, node_item.select_one(".link")["href"]),
        "photo_url": urljoin(url, node_item.select_one(".photo img")["data-original"]),
        "art": node_item.select_one(".art > strong").text.strip(),
        "price": node_item.select_one(".price > .value").text.strip(),
    }

    return data


def get_parsed_items(url, root) -> [dict]:
    return [
        parse_item(url, item)
        for item in root.select("#catalog_section .catalog-item")
    ]


if __name__ == "__main__":
    from bs4 import BeautifulSoup

    url = "https://lavkagsm.ru/catalog/mikroskhemy/?view=blocks&page_count=48&sort=name&by=asc"

    html_content = get_html_by_url__from_cache(url)
    root = BeautifulSoup(html_content, "html.parser")

    items = get_parsed_items(url, root)

    for i, item in enumerate(items, 1):
        print(i, item)
