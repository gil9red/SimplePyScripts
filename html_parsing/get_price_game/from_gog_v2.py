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
        f"https://catalog.gog.com/v1/catalog?"
        f"countryCode=RU&currencyCode=RUB&limit=20"
        f"&locale=ru-RU&order=desc:score"
        f"&page=1&productType=in:game,pack,dlc,extras"
        f"&query=like:{name}"
    )

    rs = session.get(url)
    rs.raise_for_status()

    data = rs.json()
    return [
        (game["title"], game["price"]["baseMoney"]["amount"])
        for game in data["products"]
        if game["price"] and game["price"]["baseMoney"]["currency"] == "RUB"
    ]


if __name__ == "__main__":
    print(get_games("titan quest"))
    # [('Titan Quest: Eternal Embers', '649.00'), ('Titan Quest: Atlantis', '449.00'), ('Titan Quest: Ragnarök', '649.00'), ('Titan Quest Anniversary Edition', '649.00')]

    print(get_games("Titan Quest: Atlantis"))
    # [('Titan Quest: Atlantis', '449.00')]

    print(get_games("Prodeus"))
    # [('Prodeus', '465.00'), ('Prodeus MIDI Soundtrack', '0.00'), ('Prodeus Soundtrack', '892.00')]

    print(get_games("Psychonauts 2"))
    # [('Psychonauts 2', '1085.00'), ('Psychonauts', '249.00')]

    print(get_games("dfsfsdfdsf"))
    # []
