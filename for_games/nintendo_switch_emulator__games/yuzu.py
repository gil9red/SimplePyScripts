#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from bs4 import BeautifulSoup
import requests


def get_games() -> list[tuple[str, str]]:
    rs = requests.get("https://yuzu-emu.org/game/")
    root = BeautifulSoup(rs.content, "html.parser")

    items = []

    for tr in root.select("table")[1].select("tr"):
        tds = tr.select("td")
        if len(tds) != 3:
            continue

        td_title, td_compatibility, _ = tds
        items.append(
            (td_title.get_text(strip=True), td_compatibility.get_text(strip=True))
        )

    return items


if __name__ == "__main__":
    games = get_games()
    print("Total:", len(games))
    # Total: 1145

    print()

    playable_games = [
        title
        for (title, compatibility) in games
        if compatibility in ("Perfect", "Great")
    ]
    print("Total playable:", len(playable_games))
    # Total playable: 301

    print()

    perfect_games = [
        title for (title, compatibility) in games if compatibility == "Perfect"
    ]
    print(f"Total perfect({len(perfect_games)}):")
    for i, title in enumerate(perfect_games, 1):
        print(f"{i}. {title}")

    # Total perfect(101):
    # ...

    import common

    file_name = common.get_json_file_name(__file__)
    common.dump(file_name, games, playable_games, perfect_games)
