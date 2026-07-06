#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os

from pathlib import Path
from dataclasses import dataclass

import requests


@dataclass
class User:
    login: str
    url: str


DIR: Path = Path(__file__).resolve().parent

TOKEN_FILE_NAME: Path = DIR / "TOKEN.txt"
try:
    TOKEN: str = os.environ.get("TOKEN") or TOKEN_FILE_NAME.read_text("utf-8").strip()
except:
    TOKEN: str = ""


session = requests.Session()

if TOKEN:
    session.headers["Authorization"] = f"Bearer {TOKEN}"


def get_users(url: str) -> list[User]:
    per_page: int = 100
    page: int = 1

    items: list[User] = []

    while True:
        params = dict(per_page=per_page, page=page)
        rs = session.get(url, params=params)
        rs.raise_for_status()

        result: list[dict] = rs.json()
        if not result:
            break

        items += [
            User(
                login=item["login"],
                url=item["html_url"],
            )
            for item in result
        ]

        page += 1

    return items
