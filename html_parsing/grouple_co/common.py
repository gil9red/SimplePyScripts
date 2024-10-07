#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import enum
import json
import re
import time

from dataclasses import dataclass, field
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

from config import LOGIN, PASSWORD


@dataclass
class Bookmark:
    title: str
    url: str
    tags: list[str] = field(default_factory=list)

    def get_title_with_tags(self) -> str:
        return self.title + (f" [{', '.join(self.tags)}]" if self.tags else "")


class AutoName(enum.Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class Status(AutoName):
    WATCHING = enum.auto()  # В процессе
    USER_DEFINED = enum.auto()  # Пользовательская
    ON_HOLD = enum.auto()  # Пока бросил
    PLANED = enum.auto()  # В планах
    COMPLETED = enum.auto()  # Готово
    FAVORITE = enum.auto()  # Любимая


HOST: str = "https://grouple.co"


session = requests.Session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0"


def get_url(uri: str) -> str:
    return urljoin(HOST, uri)


def do_get(uri: str, **kwargs) -> requests.Response:
    rs = session.get(get_url(uri), **kwargs)
    rs.raise_for_status()

    return rs


def do_post(uri: str, **kwargs) -> requests.Response:
    rs = session.post(get_url(uri), **kwargs)
    rs.raise_for_status()

    return rs


def do_auth() -> requests.Response:
    form_data = {
        "username": LOGIN,
        "password": PASSWORD,
    }

    rs = do_post("/login/authenticate", data=form_data)

    # Example: https://grouple.co/internal/auth/login?login_error=1
    if "error" in rs.url:
        raise Exception("Invalid auth!")

    return rs


def load(uri: str, **kwargs) -> requests.Response:
    # NOTE: Была замечена смена домена
    global HOST
    rs = do_get("/")
    if not rs.url.startswith(HOST):
        HOST = rs.url

    while True:
        rs = do_get(uri, **kwargs)
        time.sleep(1)

        # Если нужно авторизоваться
        if "/login/auth" in rs.url:
            do_auth()
            continue

        return rs


def parse_bookmark(el: Tag) -> Bookmark:
    tags = []
    if el.sup:
        tags += [x.get_text(strip=True).lower() for x in el.sup.select("span[class]")]

        # Удаление сноски ("Выпуск завершен", "переведено" и т.п.), чтобы в title она не попала
        el.sup.decompose()

    title = el.get_text(strip=True)
    url = el["href"]

    return Bookmark(title=title, url=url, tags=tags)


def get_bookmarks_by_status(status: Status) -> list[Bookmark]:
    rs = load("/private/bookmarks")

    m = re.search(r"var SITES = (\[.+]);", rs.text)
    if not m:
        raise Exception('Не удалось найти "var SITES = "!')

    # Example: var SITES = [{"id":1,"title":"ReadManga","url":"https://readmanga.io"}, ...
    sites_str = m.group(1)
    sites = json.loads(sites_str)
    site_id_by_url = {x["id"]: x["url"] for x in sites}

    items: list[Bookmark] = []

    limit = 50
    offset = 0

    while True:
        data = {
            "bookmarkSort": "NAME",
            "query": "",
            "elementFilter": [],
            "statusFilter": [status.value],
            "limit": limit,
            "offset": offset,
        }
        headers = {
            "Authorization": f'Bearer {session.cookies["gwt"]}',
            "Referer": rs.url,
        }
        rs = do_post("/api/bookmark/list", json=data, headers=headers)

        result = rs.json()
        for item in result["list"]:
            title = item["element"]["name"]

            site_id = item["element"]["elementId"]["siteId"]
            element_url = item["element"]["elementUrl"]
            url = site_id_by_url[site_id] + element_url

            # Example:
            #   tags_str = " <span class='mangaSingle'>Сборник</span><span class='mangaEmpty'>Online</span>"
            #   tags = ['Сборник', 'Online']
            tags_str = item["element"]["tagsString"]
            tags = [
                el.get_text(strip=True).lower()
                for el in BeautifulSoup(tags_str, "html.parser").select("span")
            ]

            items.append(
                Bookmark(title=title, url=url, tags=tags)
            )

        if result["offset"] + result["limit"] >= result["total"]:
            break

        offset += limit
        time.sleep(2)

    return items


def get_plain_all_bookmarks_from_user(user_id: int) -> list[Bookmark]:
    rs = load(f"/user/{user_id}/bookmarks")
    root = BeautifulSoup(rs.content, "html.parser")

    return [
        parse_bookmark(row)
        for row in root.select("a.site-element")
    ]


def get_all_bookmarks() -> dict[Status, list[Bookmark]]:
    return {
        status: get_bookmarks_by_status(status)
        for status in Status
    }


if __name__ == "__main__":
    assert Status.WATCHING.name == Status.WATCHING.value
    assert Status.WATCHING.name == "WATCHING"

    print(session.cookies)
    print(load("/"))
    print(do_auth())
    print(session.cookies)

    print("\n" + "-" * 50 + "\n")

    print(get_plain_all_bookmarks_from_user(315828))

    print("\n" + "-" * 50 + "\n")

    bookmarks = get_bookmarks_by_status(Status.WATCHING)
    print(f"Bookmarks ({len(bookmarks)}):")
    for i, bookmark in enumerate(bookmarks, 1):
        print(f"{i}. {bookmark}")
    """
    Bookmarks (28):
    1. Bookmark(title='Башня Бога', url='https://readmanga.io/bashnia_boga__A339d2', tags=[])
    2. Bookmark(title='Берсерк', url='https://readmanga.io/berserk', tags=[])
    3. Bookmark(title='Боруто', url='https://readmanga.io/boruto__A5327', tags=[])
    ...
    26. Bookmark(title='Священная  земля', url='https://readmanga.io/sviachennaia__zemlia__A533b', tags=['переведено'])
    27. Bookmark(title='Терраформирование', url='https://mintmanga.live/terraformirovanie__A5327', tags=[])
    28. Bookmark(title='Фейри Тейл. Начало', url='https://readmanga.io/feiri_teil__nachalo', tags=['переведено', 'Без глав'])
    """
