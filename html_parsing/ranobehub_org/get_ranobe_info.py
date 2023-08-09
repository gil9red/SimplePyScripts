#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from dataclasses import dataclass, field

from bs4 import BeautifulSoup

from common import session


def parse_characters(text: str) -> tuple[str, int]:
    title = ""
    number = 0

    if m := re.search(r"(\d+)([KM]?)\b", text.upper()):
        title = m.group()
        number, unit = m.groups()
        number = int(number)
        match unit:
            case "K":
                number *= 1_000
            case "M":
                number *= 1_000_000

    return title, number


@dataclass
class Ranobe:
    title: str
    release_year: int
    country: str
    status: str
    characters: str
    characters_number: int = field(repr=False)
    genres: list[str] = field(default_factory=list, repr=False)
    tags: list[str] = field(default_factory=list, repr=False)


def get_ranobe_info(url: str) -> Ranobe:
    rs = session.get(url)
    rs.raise_for_status()

    soup = BeautifulSoup(rs.content, "html.parser")

    title = soup.select_one(".book-header .ui.huge.header").get_text(strip=True)

    release_year = 0
    country = ""
    status = ""
    characters_text = ""
    characters_number = 0

    for row in soup.select(".book-meta-row"):
        key = row.select_one(".book-meta-key").get_text(strip=True)

        value_el = row.select_one(".book-meta-value")
        value = value_el.get_text(strip=True)

        match key:
            case "Год выпуска":
                release_year = int(value)
            case "Страна":
                country = value
            case "Статус перевода":
                status = value
            case "Главы":
                chapters_info = value_el.select_one("i[data-tippy-content]")["data-tippy-content"]
                characters_text, characters_number = parse_characters(chapters_info)

    genres = [
        el.get_text(strip=True)
        for el in soup.select(".book-meta-value.book-tags > .book-tag")
    ]
    genres = sorted(set(genres))

    tags = [
        el.get_text(strip=True)
        for el in soup.select(".book-container--footer .book-tags .book-tag")
    ]
    tags = sorted(set(tags))

    return Ranobe(
        title=title,
        release_year=release_year,
        country=country,
        status=status,
        characters=characters_text,
        characters_number=characters_number,
        genres=genres,
        tags=tags,
    )


if __name__ == "__main__":
    url = "https://ranobehub.org/ranobe/72-god-and-devil-world"
    ranobe = get_ranobe_info(url)
    print(ranobe)
    # Ranobe(title='Мир Бога и Дьявола', release_year=2013, country='Китай', status='Завершено', characters='11M')

    print(f"Characters: {ranobe.characters}, number: {ranobe.characters_number}")
    # Characters: 11M, number: 11000000

    print(f"Genres: ({len(ranobe.genres)}): {ranobe.genres}")
    # Genres: (13): ['Боевые искусства', 'Гарем', 'Для взрослых', ..., 'Фэнтези', 'Экшн', 'Эччи']

    print(f"Tags: ({len(ranobe.tags)}): {ranobe.tags}")
    # Tags: (57): ['Антигерой', 'Апокалипсис', 'Армия', ..., 'Фарминг', 'Эволюция', 'Эгоистичный главный герой']
