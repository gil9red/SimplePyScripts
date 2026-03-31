#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json

from dataclasses import dataclass
from datetime import date
from typing import Any

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
    hacked_groups: str
    release_date: date
    crack_date: date

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Game":
        protection: str = data["protections"]
        if protection.startswith("["):
            protection = ", ".join(json.loads(protection))

        return cls(
            title=data["title"],
            url=f'{URL_BASE}/{data["slug"]}',
            protection=protection,
            hacked_groups=data["hacked_groups"],
            release_date=date.fromisoformat(data["release_date"]),
            crack_date=date.fromisoformat(data["crack_date"]),
        )


def get_games() -> list[Game]:
    rs = session.get(f"{URL_BASE}/back/api/gameinfo/game/lastcrackedgames/")
    rs.raise_for_status()

    return [Game.from_dict(game) for game in rs.json()["list_crack_games"]]


if __name__ == "__main__":
    items = get_games()
    print(f"Games ({len(items)}):")
    for i, game in enumerate(items, 1):
        print(f"{i}. {game}")
    """
    Games (200):
    1. Game(title='RAIDOU Remastered: The Mystery of the Soulless Army', url='https://gamestatus.info/raidou-remastered-the-mystery-of-the-soulless-army', protection='DRM', hacked_groups='DenuvOwO Hypervisor — это обход защиты, при котором обычно необходимо отключить защиту ПК, что делает ваше устройство более уязвимым. Будьте осторожны!', release_date=datetime.date(2025, 6, 18), crack_date=datetime.date(2026, 3, 31))
    2. Game(title="Sid Meier's Civilization® VII - Founders Edition", url='https://gamestatus.info/sid-meiers-civilization-vii', protection='Denuvo Anti-tamper', hacked_groups='DenuvOwO Hypervisor — это обход защиты, при котором обычно необходимо отключить защиту ПК, что делает ваше устройство более уязвимым. Будьте осторожны!', release_date=datetime.date(2025, 2, 10), crack_date=datetime.date(2026, 3, 31))
    3. Game(title='Persona 4 Arena Ultimax', url='https://gamestatus.info/persona-4-arena-ultimax', protection='DENUVO', hacked_groups='DenuvOwO Hypervisor — это обход защиты, при котором обычно необходимо отключить защиту ПК, что делает ваше устройство более уязвимым. Будьте осторожны!', release_date=datetime.date(2022, 3, 16), crack_date=datetime.date(2026, 3, 30))
    4. Game(title='SUPER ROBOT WARS Y', url='https://gamestatus.info/super-robot-wars-y', protection='Denuvo Anti-Tamper', hacked_groups='DenuvOwO Hypervisor — это обход защиты, при котором обычно необходимо отключить защиту ПК, что делает ваше устройство более уязвимым. Будьте осторожны!', release_date=datetime.date(2025, 8, 27), crack_date=datetime.date(2026, 3, 30))
    5. Game(title='Hozy', url='https://gamestatus.info/hozy', protection='STEAM', hacked_groups='RUNE', release_date=datetime.date(2026, 3, 30), crack_date=datetime.date(2026, 3, 30))
    ...
    198. Game(title='Under The Island', url='https://gamestatus.info/under-the-island', protection='GOG', hacked_groups='DRM-Free', release_date=datetime.date(2026, 2, 17), crack_date=datetime.date(2026, 2, 17))
    199. Game(title='Fisherman Simulator', url='https://gamestatus.info/fisherman-simulator', protection='STEAM', hacked_groups='Tenoke', release_date=datetime.date(2026, 2, 13), crack_date=datetime.date(2026, 2, 17))
    200. Game(title='Styx: Blades of Greed', url='https://gamestatus.info/styx-blades-of-greed', protection='STEAM', hacked_groups='RUNE', release_date=datetime.date(2026, 2, 19), crack_date=datetime.date(2026, 2, 17))
    """
