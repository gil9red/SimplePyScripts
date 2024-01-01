#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests


session = requests.Session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"


def get_games(name: str) -> list[tuple[str, str]]:
    url = (
        "https://www.gog.com/games/ajax/filtered?"
        f"language=ru&mediaType=game&page=1&search={name}"
    )

    rs = session.get(url)
    rs.raise_for_status()

    data = rs.json()

    return [
        (game["title"], game["price"]["baseAmount"])
        for game in data["products"]
    ]


if __name__ == "__main__":
    print(get_games("titan quest"))
    # [('Titan Quest: Eternal Embers', '649'), ('Titan Quest Anniversary Edition', '649'), ('Titan Quest: Atlantis', '449'), ('Titan Quest: Ragnarök', '649')]

    print(get_games("Titan Quest: Atlantis"))
    # [('Titan Quest: Atlantis', '449')]

    print(get_games("Prodeus"))
    # [('Prodeus', '465')]

    print(get_games("dfsfsdfdsf"))
    # []
