#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json

from dataclasses import dataclass
from datetime import date

import requests


session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0"


URL_BASE = "https://gamestatus.info"


@dataclass
class Game:
    title: str
    url: str
    protection: str
    release_date: date
    crack_date: date

    @classmethod
    def parse_from(cls, data: dict) -> "Game":
        # Example: "[\"DENUVO\"]" -> "DENUVO", "denuvo" -> "DENUVO"
        protection: str = data["protections"].upper()
        if protection.startswith("["):
            protection = ", ".join(json.loads(protection))

        return cls(
            title=data["title"],
            url=f'{URL_BASE}/{data["slug"]}',
            protection=protection,
            release_date=date.fromisoformat(data["release_date"]),
            crack_date=date.fromisoformat(data["crack_date"]),
        )


def get_games() -> list[Game]:
    rs = session.get(f"{URL_BASE}/back/api/gameinfo/game/lastcrackedgames/")
    rs.raise_for_status()

    return [Game.parse_from(game) for game in rs.json()["list_crack_games"]]


if __name__ == "__main__":
    items = get_games()
    print(f"Games ({len(items)}):")
    for i, game in enumerate(items, 1):
        print(f"{i}. {game}")
    """
    Games (200):
    1. Game(title='High On Life', url='https://gamestatus.info/high-on-life', protection='STEAM', release_date=datetime.date(2022, 12, 13), crack_date=datetime.date(2022, 12, 13))
    2. Game(title='CRISIS CORE –FINAL FANTASY VII– REUNION', url='https://gamestatus.info/crisis-core-final-fantasy-vii-reunion', protection='STEAM', release_date=datetime.date(2022, 12, 13), crack_date=datetime.date(2022, 12, 13))
    3. Game(title='Wavetale', url='https://gamestatus.info/wavetale', protection='STEAM', release_date=datetime.date(2022, 12, 12), crack_date=datetime.date(2022, 12, 12))
    ...
    198. Game(title='Spire of Sorcery', url='https://gamestatus.info/spire-of-sorcery', protection='STEAM', release_date=datetime.date(2021, 10, 21), crack_date=datetime.date(2021, 10, 21))
    199. Game(title='Inscryption', url='https://gamestatus.info/Inscryption', protection='STEAM', release_date=datetime.date(2021, 10, 19), crack_date=datetime.date(2021, 10, 19))
    200. Game(title='Youtubers Life 2', url='https://gamestatus.info/youtubers-life-2', protection='STEAM', release_date=datetime.date(2021, 10, 19), crack_date=datetime.date(2021, 10, 19))
    """
