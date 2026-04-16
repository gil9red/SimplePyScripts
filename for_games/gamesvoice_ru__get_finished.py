#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
from datetime import datetime, date
from typing import Any

import requests


@dataclass
class Game:
    title_eng: str
    title_rus: str | None
    url: str
    published_at: date


session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"


def get_games() -> list[Game]:
    rs = session.get(
        "https://api.gamesvoice.ru/api/products/all",
        params=dict(
            is_develop=0,
            not_by_published=1,  # По дате выхода (новые-старые)
        ),
    )
    rs.raise_for_status()

    result: dict[str, Any] = rs.json()
    assert result.get("success"), "Получен неуспешный ответ"

    # NOTE Пример obj:
    """
    {
        "id": 7,
        "title_eng": "Alan Wake II",
        "title_rus": null,
        "preview": "https://api.gamesvoice.ru/storage/uploads/products/previews/37c4e26ba5c1b074367b6a8d2c53ad3e.png",
        "search_preview": "https://api.gamesvoice.ru/storage/uploads/products/search_previews/0f590f1f3951cdd1c6271c8af62ef431.png",
        "search_description": "\u003Cp\u003EAlan Wake II &mdash; это игра в жанре survival-horror от третьего лица. Игрокам предсто",
        "alias": "alanwake2",
        "published_at": "2025-04-17 00:00:00",
        "renewal_at": "2025-05-05 00:00:00"
    }
    """
    return [
        Game(
            title_eng=obj["title_eng"],
            title_rus=obj["title_rus"],
            url=f"https://www.gamesvoice.ru/product/{obj['alias']}",
            published_at=datetime.fromisoformat(obj["published_at"]).date(),
        )
        for obj in result["data"]
    ]


if __name__ == "__main__":
    items = get_games()
    print(f"Games ({len(items)}):")
    for i, game in enumerate(items, 1):
        print(f"  {i}. {game}")
    """
    Games (71):
      1. Game(title_eng='Volkolak: The Will of Gods', title_rus='Волколак: Воля Богов', url='https://www.gamesvoice.ru/product/volkolak', published_at=datetime.date(2025, 8, 22))
      2. Game(title_eng='One-Eyed Likho', title_rus='ЛИХО ОДНОГЛАЗОЕ', url='https://www.gamesvoice.ru/product/likho', published_at=datetime.date(2025, 7, 28))
      3. Game(title_eng='Silent Hill 2', title_rus='Сайлент Хилл 2', url='https://www.gamesvoice.ru/product/silenthill2', published_at=datetime.date(2025, 6, 28))
      ...
      69. Game(title_eng='Panzer Corps', title_rus=None, url='https://www.gamesvoice.ru/product/panzercorps', published_at=datetime.date(2012, 7, 8))
      70. Game(title_eng='Mad Riders', title_rus=None, url='https://www.gamesvoice.ru/product/madriders', published_at=datetime.date(2012, 7, 3))
      71. Game(title_eng='Defenders of Ardania', title_rus=None, url='https://www.gamesvoice.ru/product/doa', published_at=datetime.date(2012, 5, 26))
    """
