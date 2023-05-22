#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import time

from dataclasses import dataclass, field, asdict
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag


@dataclass
class Episode:
    title: str
    url: str
    img_url: str
    description: str


@dataclass
class Season:
    title: str
    url: str
    cover_url: str
    episodes: list[Episode] = field(default_factory=list, repr=False)

    number_of_episodes: int = 0

    def __getattribute__(self, item):
        if item == "number_of_episodes":
            return len(self.episodes)
        return super().__getattribute__(item)


def _json_default(obj):
    if isinstance(obj, (Episode, Season)):
        return asdict(obj)

    return obj


def parse_episode(episode: Tag) -> Episode:
    title = episode.select_one(".bshead h2").get_text(strip=True)
    url = episode.select_one(".mlink a")["href"]
    img_url = episode.select_one(".sstory > .highslide")["href"]
    description = "\n".join(
        p.get_text(strip=True) for p in episode.select(".sstory > p")
    )

    return Episode(title, url, img_url, description)


def parse() -> list[Season]:
    url = "http://online-south-park.ru/"

    s = requests.session()
    rs = s.get(url)
    root = BeautifulSoup(rs.content, "html.parser")

    seasons = []

    for cell in root.select_one(".alltable").select(".cell"):
        title = cell.p.get_text(strip=True)
        season_url = urljoin(rs.url, cell.a["href"])
        cover_url = urljoin(rs.url, cell.a.img["src"])
        episodes = []

        seasons.append(Season(title, season_url, cover_url, episodes))

        while True:
            rs_season = s.get(season_url)
            root = BeautifulSoup(rs_season.content, "html.parser")
            for episode in root.select(".base.shortstory"):
                episodes.append(parse_episode(episode))

            # Поиск панели навигации между страницами с эпизодами
            nextprev_el = root.select_one(".nextprev")
            if not nextprev_el:
                break

            _, next_el = nextprev_el.children

            # Если нет больше страниц
            if not next_el.has_attr("href"):
                break

            season_url = next_el["href"]

        # Не нужно напрягать сайт
        time.sleep(1)

    return seasons


if __name__ == "__main__":
    seasons = parse()
    print("Total seasons:", len(seasons))
    print("Total episodes:", sum(s.number_of_episodes for s in seasons))

    json.dump(
        seasons,
        open("seasons.json", "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
        default=_json_default,
    )
