#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag


@dataclass
class Game:
    name: str
    url: str
    date_str: str


def get_text(el: Tag) -> str:
    if not el:
        return ""
    return el.get_text().replace("\u200b", " ").replace("\xa0", " ").strip()


session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"


def get_games() -> list[Game]:
    url = "https://www.gamesvoice.ru/"

    rs = session.get(url)
    rs.raise_for_status()

    items: list[Game] = []

    soup = BeautifulSoup(rs.content, "html.parser")
    for section in soup.select("section[data-block-level-container='ClassicSection']"):
        if "Локализации и озвучки GamesVoice" not in section.text:
            continue

        for item in section.select(".wixui-repeater__item > div > div"):
            divs = item.find_all("div")

            # Поиск по структуре
            if len(divs) != 3:
                continue

            div_url, div_name, div_date = divs

            a_el = div_url.select_one("a[href]")
            name = get_text(div_name.select_one("h4"))
            date_str = get_text(div_date.select_one("h1"))

            if not a_el or not name or not date_str:
                continue

            items.append(
                Game(
                    name=name,
                    url=urljoin(rs.url, a_el["href"]),
                    date_str=date_str,
                )
            )

    return items


if __name__ == "__main__":
    items = get_games()
    print(f"Games ({len(items)}):")
    for i, game in enumerate(items, 1):
        print(f"  {i}. {game}")
    """
    Games (55):
      1. Game(name='A Plague Tale: Innocence', url='https://www.gamesvoice.ru/innocence', date_str='11 марта 2024')
      2. Game(name='Close to the Sun', url='https://www.gamesvoice.ru/closetothesun', date_str='27 февраля 2024')
      3. Game(name='Tomb Raider I-III Remastered', url='https://www.gamesvoice.ru/tomb-raider-remastered', date_str='14 февраля 2024')
      ...
      53. Game(name='Panzer Corps', url='https://www.gamesvoice.ru/panzercorps', date_str='8 июля 2012')
      54. Game(name='Mad Riders', url='https://www.gamesvoice.ru/madriders', date_str='3 июля 2012')
      55. Game(name='Defenders of Ardania', url='https://www.gamesvoice.ru/doa', date_str='26 мая 2012')
    """

    assert items, "Empty list"
    for game in [
        Game(
            name="A Plague Tale: Innocence",
            url="https://www.gamesvoice.ru/innocence",
            date_str="11 марта 2024",
        ),
        Game(
            name="Defenders of Ardania",
            url="https://www.gamesvoice.ru/doa",
            date_str="26 мая 2012",
        ),
    ]:
        assert game in items, f"Game not found: {game}"
