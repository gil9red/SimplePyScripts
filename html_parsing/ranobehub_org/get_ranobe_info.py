#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import re

from dataclasses import dataclass, field
from typing import Any

from bs4 import BeautifulSoup, Tag

from common import session, get_text


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
    parser_version: str = "v1"

    def __post_init__(self) -> None:
        self.genres = sorted(set(self.genres))
        self.tags = sorted(set(self.tags))


def parse_book_v1(soup: BeautifulSoup) -> Ranobe:
    title: str = get_text(soup.select_one(".book-header .ui.huge.header"))
    release_year: int = 0
    country: str = ""
    status: str = ""
    characters_text: str = "-"
    characters_number: int = -1
    genres: list[str]
    tags: list[str]

    for row in soup.select(".book-meta-row"):
        key: str = get_text(row.select_one(".book-meta-key"))

        value_el = row.select_one(".book-meta-value")
        value = get_text(value_el)

        match key:
            case "Год выпуска":
                release_year = int(value)
            case "Страна":
                country = value
            case "Статус перевода":
                status = value
            case "Главы":
                value_content_el = value_el.select_one("i[data-tippy-content]")
                chapters_info = value_content_el["data-tippy-content"]
                characters_text, characters_number = parse_characters(chapters_info)

    genres = [
        get_text(el) for el in soup.select(".book-meta-value.book-tags > .book-tag")
    ]
    tags = [
        get_text(el)
        for el in soup.select(".book-container--footer .book-tags .book-tag")
    ]

    return Ranobe(
        title=title,
        release_year=release_year,
        country=country,
        status=status,
        characters=characters_text,
        characters_number=characters_number,
        genres=genres,
        tags=tags,
        parser_version="v1",
    )


def parse_book_v2(soup: BeautifulSoup) -> Ranobe:
    title = get_text(soup.select_one(".book-overview h1"))
    genres: list[str]
    tags: list[str]

    year_tag: Tag | None = soup.select_one(".book-kicker-year[href*=year]")
    if not year_tag:
        raise ValueError("Year tag not found")

    year_href: str = year_tag["href"]

    m = re.search(r"/year/(\d+)", year_href)
    if not m:
        raise ValueError(f"Year not found in {year_href!r}")
    year_str: str = m.group(1)
    release_year: int = int(year_str)

    country: str = get_text(soup.select_one(".book-kicker-country[href*=country]"))
    status: str = get_text(soup.select_one(".book-kicker-status[href*=status]"))

    # NOTE: Не нашел в верстке
    characters_text: str = "-"
    characters_number: int = -1

    # NOTE: Example <script>self.__next_f.push([1, "5:[...]"])</script>
    #                                                   ^
    #                                ["$","section",null,{"className": ...}]
    slice_genres_tags: str = ""
    for slice in re.findall(
        r"""<script>self.__next_f.push\((\[.+?\])\).*?</script>""", str(soup)
    ):
        if "book-hero-taxonomy" in slice:
            slice_genres_tags = slice
            break
    if not slice_genres_tags:
        raise ValueError("Не найден book-hero-taxonomy в self.__next_f")

    _, slice_data = json.loads(slice_genres_tags)

    _, data_str = slice_data.split(":", maxsplit=1)

    # NOTE: Example ["$","section",null,{"className": ...}]
    data: dict[str, Any]
    _, _, _, data = json.loads(data_str)

    assert isinstance(data, dict), f"В data не словарь, а {type(data)}: {data!r}"

    def deep_find(
        data: dict[str, Any],
        has_key: str,
        has_value: str,
        target_key: str,
    ) -> Any:
        if isinstance(data, dict):
            if data.get(has_key) == has_value and target_key in data:
                return data[target_key]
            for value in data.values():
                result = deep_find(
                    value, has_key=has_key, has_value=has_value, target_key=target_key
                )
                if result is not None:
                    return result
        elif isinstance(data, list):
            for item in data:
                result = deep_find(
                    item, has_key=has_key, has_value=has_value, target_key=target_key
                )
                if result is not None:
                    return result
        return None

    data_children: list[tuple[str, str, Any, dict]] | None = deep_find(
        data,
        has_key="className",
        has_value="book-hero-taxonomy",
        target_key="children",
    )
    assert data_children, "Не найден класс book-hero-taxonomy в data"
    assert isinstance(data_children, list), "Не найден список children в data"

    all_genres: list[str] = []
    all_tags: list[str] = []

    # NOTE: Example
    """
    [
        '$', 'div', None,
        {
            'className': 'book-hero-taxonomy',
            'children': [
                [
                    '$', 'nav', None,
                    {
                        'aria-label': 'Жанры произведения',
                        'children': [
                            ['$', 'span', None, {'children': [[...], ' Жанры']}],
                            [
                                ['$', '$L2a', '5', {'bookId': 345, 'href': '/tag/5', 'children': 'Сэйнэн'}],
                                ...,
                            ]
                        ]
                    }
                ],
                [
                    '$', 'nav', None,
                    {
                        'aria-label': 'Темы произведения',
                        'children': [
                            [...],
                            [
                                ['$', '$L2a', '6', {'bookId': 345, 'href': '/tag/6', 'children': 'Демоны'}],
                                ...,
                            ]
                        ]
                    }
                ],
                [
                    '$', '$L39', None,
                    {
                        'bookId': 345,
                        'genres': [
                            {'id': 17, 'title': 'Комедия'},
                            ...,
                        ],
                        'labels': [
                            {'id': 38, 'title': 'Магия'},
                            ...,
                        ]
                    }
                ]
            ]
        }
    ]
    """
    for _, _, _, item in data_children:
        assert isinstance(item, dict), f"data/children[]/item[3] is not dict: {item!r}"

        aria_label: str | None = item.get("aria-label")
        if aria_label:

            def extract_titles_from_children(
                data_aria_label: dict[str, Any],
            ) -> list[str]:
                values = data_aria_label.get("children")
                assert isinstance(
                    values, list
                ), f"data/children[]/item[3]/children[] is not list: {values!r}"

                items: list[str] = []
                for row in values:
                    if not isinstance(row[0], list):
                        continue

                    for _, _, _, value in row:
                        if (
                            isinstance(value, dict)
                            and "/tag/" in value.get("href", "")
                            and isinstance(value.get("children"), str)
                        ):
                            items.append(value["children"])

                return items

            match aria_label:
                case "Жанры произведения":
                    all_genres += extract_titles_from_children(item)
                    pass
                case "Темы произведения":
                    all_tags += extract_titles_from_children(item)
                    pass

        else:

            def extract_titles(key: str) -> list[str]:
                values = item.get(key)
                assert isinstance(
                    values, list
                ), f"data/children[]/item[3]/{key}[] is not list: {values!r}"
                return [value["title"] for value in values]

            all_genres += extract_titles("genres")
            all_tags += extract_titles("labels")

    return Ranobe(
        title=title,
        release_year=release_year,
        country=country,
        status=status,
        characters=characters_text,
        characters_number=characters_number,
        genres=all_genres,
        tags=all_tags,
        parser_version="v2",
    )


def get_ranobe_info(url: str) -> Ranobe:
    rs = session.get(url)
    rs.raise_for_status()

    soup = BeautifulSoup(rs.content, "html.parser")

    try:
        return parse_book_v2(soup)
    except AttributeError:
        return parse_book_v1(soup)


if __name__ == "__main__":
    url = "https://ranobehub.org/ranobe/72-god-and-devil-world"
    ranobe = get_ranobe_info(url)
    print(ranobe)
    print(f"Characters: {ranobe.characters}, number: {ranobe.characters_number}")
    print(f"Genres: ({len(ranobe.genres)}): {ranobe.genres}")
    print(f"Tags: ({len(ranobe.tags)}): {ranobe.tags}")
    """
    Ranobe(title='Мир Бога и Дьявола', release_year=2013, country='Китай', status='Завершено', characters='11M', parser_version='v1')
    Characters: 11M, number: 11000000
    Genres: (13): ['Боевые искусства', 'Гарем', 'Для взрослых', ..., 'Фэнтези', 'Экшн', 'Эччи']
    Tags: (57): ['Антигерой', 'Апокалипсис', 'Армия', ..., 'Фарминг', 'Эволюция', 'Эгоистичный главный герой']
    """

    print("\n" + "-" * 100 + "\n")

    url = "https://ranobehub.org/ranobe/345-overgeared"
    ranobe = get_ranobe_info(url)
    print(ranobe)
    print(f"Characters: {ranobe.characters}, number: {ranobe.characters_number}")
    print(f"Genres: ({len(ranobe.genres)}): {ranobe.genres}")
    print(f"Tags: ({len(ranobe.tags)}): {ranobe.tags}")
    """
    Ranobe(title='Во всеоружии', release_year=2014, country='Корея', status='Завершено', characters='-', parser_version='v2')
    Characters: -, number: -1
    Genres: (6): ['Гарем', 'Комедия', 'Приключение', 'Сэйнэн', 'Фэнтези', 'Экшн']
    Tags: (104): ['Ад', 'Алхимия', 'Ангелы', ..., 'Хозяин подземелий', 'Элементальная магия', 'Эльфы']
    """
