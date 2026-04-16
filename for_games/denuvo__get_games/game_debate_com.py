#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"


def get_games() -> list[tuple[str, str]]:
    items = []

    rs = session.get("https://www.game-debate.com/games/gamesWithDenuvo")
    rs.raise_for_status()

    root = BeautifulSoup(rs.content, "html.parser")
    for el in root.select(".hasDenuvoBodyContainer > .rowContainer > a"):
        title = el.select_one(".hasDenuvo-GameTitle").get_text(strip=True)
        status = el.select_one(".hasDenuvo-DenuvoStatus").get_text(strip=True)

        items.append((title, status))

    return items


if __name__ == "__main__":
    games = get_games()
    print(f"Total games: {len(games)}")
    # Total games: 262

    uses_denuvo = [game for game, status in games if "Uses" in status]
    print(f"Uses denuvo ({len(uses_denuvo)}): {uses_denuvo[0]!r} - {uses_denuvo[1]!r}")
    # Uses denuvo (232): 'Monster Hunter Rise' - 'Battlefield 2042'

    denuvo_removed = [game for game, status in games if "Uses" not in status]
    print(
        f"Denuvo removed ({len(denuvo_removed)}): {denuvo_removed[0]!r} - {denuvo_removed[1]!r}"
    )
    # Denuvo removed (30): 'Sniper: Ghost Warrior Contracts' - 'Mutant Year Zero: Road to Eden'
