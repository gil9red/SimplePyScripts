#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests


def get_games() -> list[tuple[str, list[str]]]:
    url = "https://github.com/Ryujinx/Ryujinx-Games-List/issues"
    session = requests.session()

    items = []

    while True:
        rs = session.get(url)
        root = BeautifulSoup(rs.content, "html.parser")

        for div in root.select("div[id]"):
            if not div.has_attr("id") or not div["id"].startswith("issue_"):
                continue

            title = div.select_one('[data-hovercard-type="issue"]').get_text(strip=True)
            labels = [x.get_text(strip=True) for x in div.select(".IssueLabel")]

            items.append((title, labels))

        next_page_el = root.select_one(".pagination > .next_page")
        if not next_page_el.has_attr("href"):
            break

        url = urljoin(url, next_page_el["href"])
        time.sleep(1)

    return items


if __name__ == "__main__":
    games = get_games()
    print("Total:", len(games))
    # Total: 2011

    print()

    playable_games = [title for (title, labels) in games if "status-playable" in labels]
    print("Total playable:", len(playable_games))
    # Total playable: 677

    print()

    # Ignore problems games: slow, audio, etc.
    perfect_games = [
        title
        for (title, labels) in games
        if len(labels) == 1 and "status-playable" in labels
    ]
    print(f"Total perfect({len(perfect_games)}):")
    for i, title in enumerate(perfect_games, 1):
        print(f"{i}. {title}")

    # Total perfect(435):
    # ...

    import common

    file_name = common.get_json_file_name(__file__)
    common.dump(file_name, games, playable_games, perfect_games)
