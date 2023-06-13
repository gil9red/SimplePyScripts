#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass

from common import session


@dataclass
class Bookmark:
    title: str
    url: str
    status: str


def get_bookmarks(user_id: int) -> list[Bookmark]:
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
