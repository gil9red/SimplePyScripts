#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"


def get_games() -> list[tuple[str, bool]]:
    items = []

    rs = session.get("https://gamicus.fandom.com/wiki/Denuvo")
    rs.raise_for_status()

    root = BeautifulSoup(rs.content, "html.parser")
    for tr_el in root.select("#yesdenuvo tr"):
        td_els = tr_el.select("td")
        if not td_els:
            continue

        title = td_els[0].get_text(strip=True)
        is_cracked = "Yes" in td_els[-1].get_text(strip=True)
        items.append((title, is_cracked))

    is_cracked = True
    for tr_el in root.select("#nodenuvo tr"):
        td_els = tr_el.select("td")
        if not td_els:
            continue

        title = td_els[0].get_text(strip=True)
        items.append((title, is_cracked))

    return items


if __name__ == "__main__":
    games = get_games()
    print(f"Total games: {len(games)}")
    # Total games: 151

    with_denuvo = [game for game, is_cracked in games if not is_cracked]
    print(f"With denuvo ({len(with_denuvo)}): {with_denuvo[0]!r} - {with_denuvo[1]!r}")
    # With denuvo (32): 'Star Wars: Battlefront' - 'Plants vs. Zombies: Garden Warfare 2'

    cracked = [game for game, is_cracked in games if is_cracked]
    print(f"Cracked ({len(cracked)}): {cracked[0]!r} - {cracked[1]!r}")
    # Cracked (119): 'FIFA 15' - 'Dragon Age: Inquisition'
