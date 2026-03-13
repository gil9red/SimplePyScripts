#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import re

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Self
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

from common import DIR_DUMPS, session


FILE_NAME: Path = Path(__file__).resolve()


@dataclass
class Model:
    title: str
    url: str
    size: str
    context: str
    input: str
    id_hash: str
    last_modified: str

    @classmethod
    def parse_from(cls, item: Tag, base_url: str) -> Self:
        first_div, second_div = item.find_all("div", recursive=False)

        cell_name, cell_size, cell_context, cell_input = first_div.find_all(
            recursive=False
        )

        id_hash, last_modified = re.split(r"·", second_div.get_text(strip=True))
        id_hash = id_hash.strip()
        last_modified = last_modified.strip()

        return cls(
            title=cell_name.a.get_text(strip=True),
            url=urljoin(base_url, cell_name.a["href"]),
            size=cell_size.get_text(strip=True),
            context=cell_context.get_text(strip=True),
            input=cell_input.get_text(strip=True),
            id_hash=id_hash,
            last_modified=last_modified,
        )


session = requests.Session()


def process(name: str, file_name: Path):
    url: str = f"https://ollama.com/library/{name}/tags"
    print(f"Load: {url}")

    rs = session.get(url)
    rs.raise_for_status()

    soup = BeautifulSoup(rs.content, "html.parser")

    items: list[Model] = []
    for item in soup.select("div.group > div:has(a)"):
        model = Model.parse_from(item, base_url=rs.url)
        print(model)
        items.append(model)

    print(f"Writing to file: {FILE_NAME}")
    with open(file_name, "w", encoding="UTF-8") as f:
        for model in sorted(items, key=lambda x: x.title):
            f.write(json.dumps(asdict(model), ensure_ascii=False) + "\n")


if __name__ == "__main__":
    import time

    for name in [
        "qwen3.5",
        "qwen3-vl",
        "qwen3",
        "qwen",
        "bge-m3",
        "granite3.2-vision",
    ]:
        path_dump: Path = DIR_DUMPS / f"{FILE_NAME.name}_{name}.jsonl"
        process(name=name, file_name=path_dump)
        print()

        time.sleep(1)
