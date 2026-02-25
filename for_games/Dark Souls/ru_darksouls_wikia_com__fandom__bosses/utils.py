#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import sqlite3
import os

from collections import defaultdict
from typing import Dict, List, NamedTuple, Tuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


session = requests.Session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"


class Boss(NamedTuple):
    name: str
    url: str

    def get_boss_items(self) -> Dict[str, List[str]]:
        _, root = parse(self.url)

        key_by_values = dict()
        for table in root.select("table.pi-horizontal-group"):
            el_items = table.select_one("tbody td[data-source]")
            if not el_items:
                continue

            data_source = el_items["data-source"]
            items = [
                x.strip()
                for x in el_items.get_text(strip=True, separator="\n").split("\n")
            ]

            key_by_values[data_source] = items

        return key_by_values


def parse(url: str) -> Tuple[requests.Response, BeautifulSoup]:
    rs = session.get(url)
    return rs, BeautifulSoup(rs.content, "html.parser")


def get_bosses(url: str) -> Dict[str, List[Boss]]:
    rs, root = parse(url)

    bosses_by_category = defaultdict(list)

    category_name = None

    for tr in root.select("table tr"):
        # Заголовок первым идет
        th = tr.select_one("th")
        if th:
            category_name = th.text.strip().upper()
            continue

        if not category_name:
            continue

        td_list = []

        for td in tr.select("td"):
            name = td.text.strip()
            if not name:
                continue

            url = urljoin(rs.url, td.select_one("a")["href"])
            boss = Boss(name, url)

            td_list.append(boss)

        bosses_by_category[category_name] += td_list

    return bosses_by_category


def print_bosses(url: str, bosses: Dict[str, List[Boss]]) -> None:
    total = sum(len(i) for i in bosses.values())
    print(f"{url} ({total}):")

    for category, bosses in bosses.items():
        print(f"{category} ({len(bosses)}):")

        for i, boss in enumerate(bosses, 1):
            print(f'    {i}. "{boss.name}": {boss.url}')

        print()

    print()


def convert_bosses_to_only_name(bosses: Dict[str, List[Boss]]) -> Dict[str, List[str]]:
    bosses_only_name = dict()
    for category, bosses_list in bosses.items():
        bosses_only_name[category] = [boss.name for boss in bosses_list]

    return bosses_only_name


def export_to_json(file_name, bosses) -> None:
    dir_name = os.path.dirname(file_name)
    os.makedirs(dir_name, exist_ok=True)

    json.dump(
        bosses,
        open(file_name, mode="w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
    )


def export_to_sqlite(file_name: str, bosses_ds123: Dict[str, Dict[str, List[Boss]]]) -> None:
    dir_name = os.path.dirname(file_name)
    os.makedirs(dir_name, exist_ok=True)

    connect = sqlite3.connect(file_name)

    connect.executescript("""
        DROP TABLE IF EXISTS Boss;

        CREATE TABLE Boss (
            id INTEGER PRIMARY KEY,
            game TEXT,
            category TEXT,
            name TEXT,
            url TEXT
        );
    """)

    for game, categories in bosses_ds123.items():
        for category, bosses in categories.items():
            for boss in bosses:
                connect.execute(
                    "INSERT INTO Boss (game, category, name, url) VALUES (?, ?, ?, ?)",
                    (game, category, boss.name, boss.url),
                )

    connect.commit()
