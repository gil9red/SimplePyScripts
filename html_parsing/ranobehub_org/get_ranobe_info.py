#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass

from bs4 import BeautifulSoup

from common import session


@dataclass
class Ranobe:
    title: str
    release_year: int
    country: str
    status: str


def get_ranobe_info(url: str) -> Ranobe:
    rs = session.get(url)
    rs.raise_for_status()

    soup = BeautifulSoup(rs.content, "html.parser")

    title = soup.select_one('.book-header .ui.huge.header').get_text(strip=True)

    release_year = 0
    country = ""
    status = ""
    for row in soup.select(".book-meta-row"):
        key = row.select_one('.book-meta-key').get_text(strip=True)
        value = row.select_one('.book-meta-value').get_text(strip=True)

        match key:
            case "Год выпуска":
                release_year = int(value)
            case "Страна":
                country = value
            case "Статус перевода":
                status = value

    return Ranobe(
        title=title,
        release_year=release_year,
        country=country,
        status=status,
    )


if __name__ == '__main__':
    url = 'https://ranobehub.org/ranobe/72-god-and-devil-world'
    ranobe = get_ranobe_info(url)
    print(ranobe)
    # Ranobe(title='Мир Бога и Дьявола', release_year=2013, country='Китай', status='Завершено')
