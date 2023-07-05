#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass, field

from bs4 import BeautifulSoup

from common import session


@dataclass
class Ranobe:
    title: str
    release_year: int
    country: str
    status: str
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
    for row in soup.select(".book-meta-row"):
        key = row.select_one(".book-meta-key").get_text(strip=True)
        value = row.select_one(".book-meta-value").get_text(strip=True)

        match key:
            case "Год выпуска":
                release_year = int(value)
            case "Страна":
                country = value
            case "Статус перевода":
                status = value

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
        genres=genres,
        tags=tags,
    )


if __name__ == "__main__":
    url = "https://ranobehub.org/ranobe/72-god-and-devil-world"
    ranobe = get_ranobe_info(url)
    print(ranobe)
    # Ranobe(title='Мир Бога и Дьявола', release_year=2013, country='Китай', status='Завершено')

    print(f"Genres: ({len(ranobe.genres)}): {ranobe.genres}")
    # Genres: (13): ['Боевые искусства', 'Гарем', 'Для взрослых', ..., 'Фэнтези', 'Экшн', 'Эччи']

    print(f"Tags: ({len(ranobe.tags)}): {ranobe.tags}")
    # Tags: (57): ['Антигерой', 'Апокалипсис', 'Армия', ..., 'Фарминг', 'Эволюция', 'Эгоистичный главный герой']
