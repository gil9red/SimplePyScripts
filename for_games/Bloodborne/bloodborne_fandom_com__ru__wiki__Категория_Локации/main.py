#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import time
import sys

from dataclasses import dataclass
from urllib.parse import urljoin
from pathlib import Path

import requests
from bs4 import BeautifulSoup, Tag


DIR: Path = Path(__file__).resolve().parent

sys.path.append(
    str(DIR.parent.parent / "Dark Souls" / "generate_HTML_location_graph__with_d3js")
)
from generate_graph_html import generate as generate_graph_html


DIR_DUMPS: Path = DIR / "dumps"
DIR_DUMPS.mkdir(parents=True, exist_ok=True)

URL: str = "https://bloodborne.fandom.com/ru/wiki/Категория:Локации"


@dataclass
class Location:
    title: str
    url: str

    @classmethod
    def from_tag(cls, tag: Tag) -> "Location":
        return cls(
            title=tag["title"],
            url=urljoin(URL, tag["href"]),
        )


links: set[tuple[str, str]] = set()
location_by_url: dict[str, str] = dict()

rs = requests.get(URL)
rs.raise_for_status()

soup = BeautifulSoup(rs.content, "html.parser")
locations: list[Location] = [
    Location.from_tag(a)
    for a in soup.select("a.category-page__member-link[href][title]")
]

for location in locations:
    time.sleep(1)
    for _ in range(3):
        try:
            # TODO: Оптимизации не хватает
            rs = requests.get(location.url)
            rs.raise_for_status()
        except Exception as e:
            print(f"Error: {e}, url: {location.url}")
            time.sleep(1)

    soup = BeautifulSoup(rs.content, "html.parser")

    to_locations: list[tuple[str, str]] = [
        (a["title"], urljoin(rs.url, a["href"]))
        for a in soup.select('[data-source="Переходы"] a[href][title]')
    ]
    # У любой локации есть связанная с ней локация. Если нет - значит это страница не про локацию
    if not to_locations:
        continue

    location_by_url[location.title] = location.url

    print(location.title, location.url)
    print("    Переходы:")

    # Найдем связанные локации
    for to_title, to_url in to_locations:
        # Проверяем что ссылка ведет на локацию
        if not any(True for l in locations if l.url == to_url):  # TODO: Рефакторинг?
            continue

        print(f"        {to_title}: {to_url}")
        location_by_url[to_title] = to_url

        links.add((location.title, to_title))

print()

# Экспорт в json
location_by_url: dict[str, str] = dict(sorted(location_by_url.items()))
json.dump(
    location_by_url,
    open(DIR_DUMPS / "locations.json", "w", encoding="utf-8"),
    ensure_ascii=False,
    indent=4,
)

links: list[tuple[str, str]] = sorted(links)
json.dump(
    links,
    open(DIR_DUMPS / "locations_transitions.json", "w", encoding="utf-8"),
    ensure_ascii=False,
    indent=4,
)

generate_graph_html(
    file_name_to=DIR_DUMPS / "locations_graph.html",
    links=links,
    title="Locations Bloodborne",
)
