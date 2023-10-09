#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from bs4 import BeautifulSoup
from common import session


def get_chapter_id(url: str) -> str:
    rs = session.get(url)
    rs.raise_for_status()

    soup = BeautifulSoup(rs.content, "html.parser")
    return soup.select_one("meta[name='chapter-id']")["content"]


def get_reactions_raw(url: str) -> dict:
    params = {
        "subject_type": r"App\Entity\Chapter",
        "subject_id": get_chapter_id(url),
    }
    rs = session.get("https://ranobehub.org/api/reactions", params=params)
    rs.raise_for_status()

    return rs.json()


def get_reactions(url: str) -> dict[str, int]:
    return {
        x["reaction"]["name"]: x["interacts"]["count"]
        for x in get_reactions_raw(url)["reactions"]
    }


if __name__ == "__main__":
    print(get_reactions("https://ranobehub.org/ranobe/19/203/7"))
    # {'wow': 1, 'haha': 0, 'like': 4, 'love': 0, 'sad': 0, 'triggered': 0, 'ninja': 0, 'fuck': 1}

    print(get_reactions("https://ranobehub.org/ranobe/72/1/1"))
    # {'wow': 3, 'haha': 1, 'like': 9, 'love': 0, 'sad': 0, 'triggered': 1, 'ninja': 0, 'fuck': 0}
