#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

from dataclasses import dataclass
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from common import session, get_text


@dataclass
class Bookmark:
    title: str
    url: str
    status: str


def get_bookmarks_v1(user_id: int) -> list[Bookmark]:
    rs = session.get(f"https://ranobehub.org/user/{user_id}/library")
    rs.raise_for_status()

    rs = session.get(f"https://ranobehub.org/api/get/user/{user_id}/rate")
    rs.raise_for_status()

    items = []
    for relation in rs.json()["data"]["relations"]:
        ranobe = relation["ranobe"]
        title = ranobe["names"]["rus"]
        url = ranobe["url"]

        status = relation["status"]["title"]

        items.append(
            Bookmark(
                title=title,
                url=url,
                status=status,
            )
        )

    return items


def get_bookmarks_v2(user_id: int) -> list[Bookmark]:
    items: list[Bookmark] = []

    url: str = f"https://ranobehub.org/user/{user_id}?tab=library"

    while True:
        print(f"Загрузка страницы {url!r}")

        rs = session.get(url)
        rs.raise_for_status()

        soup = BeautifulSoup(rs.content, "html.parser")

        for item in soup.select(".profile-library-card"):
            title: str = get_text(item.select_one("h3[data-book-transition-title]"))

            rel_url: str = item.select_one("a[href]")["href"]
            abs_url: str = urljoin(rs.url, rel_url)

            status: str = get_text(
                item.select_one('[data-slot="badge"][data-variant="secondary"]')
            )
            if status not in ("Запланировано", "Прочитано"):
                raise Exception(f"Не поддерживаемый статус {status!r}")

            items.append(
                Bookmark(
                    title=title,
                    url=abs_url,
                    status=status,
                )
            )

        nav_buttons = soup.select('nav.pagination > [data-slot="button"]')
        if nav_buttons and len(nav_buttons) == 2 and nav_buttons[1].attrs.get("href"):
            rel_url: str = nav_buttons[1].attrs.get("href")
            next_url: str = urljoin(rs.url, rel_url)

            time.sleep(1)
            url = next_url
            continue

        break

    return items


def get_bookmarks(user_id: int) -> list[Bookmark]:
    try:
        return get_bookmarks_v2(user_id)
    except Exception:
        return get_bookmarks_v1(user_id)


if __name__ == "__main__":
    user_id = 19803
    bookmarks = get_bookmarks(user_id)
    print(f"Bookmarks ({len(bookmarks)}):")
    for i, bookmark in enumerate(bookmarks, 1):
        print(f"    {i}. {bookmark}")
    """ 
    Bookmarks (38):
        1. Bookmark(title='Мир Бога и Дьявола', url='https://ranobehub.org/ranobe/72-god-and-devil-world', status='Прочитано')
        2. Bookmark(title='Во всеоружии', url='https://ranobehub.org/ranobe/345-overgeared', status='Запланировано')
        3. Bookmark(title='Кровь Триединства.  Rage Against the Moons', url='https://ranobehub.org/ranobe/638-trinity-blood', status='Прочитано')
        ...
        36. Bookmark(title='Освободите эту Ведьму', url='https://ranobehub.org/ranobe/40-release-that-witch', status='Запланировано')
        37. Bookmark(title='Восстание легиона нежити', url='https://ranobehub.org/ranobe/505-rise-of-the-undead-legion', status='Запланировано')
        38. Bookmark(title='Магия вернувшегося должна быть особенной', url='https://ranobehub.org/ranobe/670-a-returners-magic-should-be-special', status='Запланировано')
    """
