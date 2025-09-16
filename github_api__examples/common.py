#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass

import requests


@dataclass
class User:
    login: str
    url: str


def get_users(url: str) -> list[User]:
    per_page: int = 100
    page: int = 1

    items: list[User] = []

    while True:
        params = dict(per_page=per_page, page=page)
        rs = requests.get(url, params=params)
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
