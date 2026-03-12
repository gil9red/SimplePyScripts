#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import time

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Self
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag


FILE_NAME: Path = Path(__file__).resolve()
DIR: Path = FILE_NAME.parent

PATH_DUMP: Path = DIR / f"{FILE_NAME.name}.jsonl"


@dataclass
class Model:
    title: str
    url: str
    description: str
    tags: list[str]
    pull_count: str
    tag_count: int
    updated: str

    @classmethod
    def parse_from(cls, item: Tag, base_url: str) -> Self:
        title_el = item.select_one("[x-test-search-response-title]")
        description: str = (
            title_el.find_next("p").get_text(strip=True) if title_el else ""
        )

        return cls(
            title=title_el.get_text(strip=True),
            url=urljoin(base_url, item["href"]),
            description=description,
            tags=[
                tag_el.get_text(strip=True)
                for tag_el in item.select("div:first-child span")
            ],
            pull_count=item.select_one("[x-test-pull-count]").get_text(strip=True),
            tag_count=int(item.select_one("[x-test-tag-count]").get_text(strip=True)),
            updated=item.select_one("[x-test-updated]").get_text(strip=True),
        )


session = requests.Session()

url: str = "https://ollama.com/search"
with open(PATH_DUMP, "w", encoding="UTF-8") as f:
    while True:
        print(f"Load: {url}")

        rs = session.get(url)
        rs.raise_for_status()

        soup = BeautifulSoup(rs.content, "html.parser")

        for item in soup.select("li[x-test-model] > a:has([x-test-search-response-title])"):
            model = Model.parse_from(item, base_url=rs.url)
            print(model)
            f.write(json.dumps(asdict(model), ensure_ascii=False) + "\n")

        f.flush()

        next_page_el: Tag | None = soup.select_one("[hx-trigger=revealed][hx-get]")
        if not next_page_el:
            break

        url = urljoin(rs.url, next_page_el["hx-get"])

        time.sleep(1)
