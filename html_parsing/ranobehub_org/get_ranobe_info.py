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
    chapters: int
    characters: int
    characters_str: str = field(repr=False)
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
    chapters: int = -1
    characters: int = -1
    characters_str: str = "-"
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
                characters_str, characters = parse_characters(chapters_info)

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
        chapters=chapters,
        characters=characters,
        characters_str=characters_str,
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

    # NOTE: Example <script>self.__next_f.push([1, "5:[...]"])</script>
    #                                                   ^
    #                                ["$","section",null,{"className": ...}]
    slice_genres_tags: str = ""
    slice_book_facts: str = ""
    for slice in re.findall(
        r"""<script>self.__next_f.push\((\[.+?\])\).*?</script>""", str(soup)
    ):
        if "book-hero-taxonomy" in slice:
            slice_genres_tags = slice
        elif "book-facts" in slice:
            slice_book_facts = slice

        if slice_genres_tags and slice_book_facts:
            break

    if not slice_genres_tags:
        raise ValueError("Не найден book-hero-taxonomy в self.__next_f")
    if not slice_book_facts:
        raise ValueError("Не найден book-facts в self.__next_f")

    # NOTE: Example ["$","section",null,{"className": ...}]
    _, slice_data = json.loads(slice_genres_tags)
    _, data_str = slice_data.split(":", maxsplit=1)
    data: dict[str, Any]
    _, _, _, data = json.loads(data_str)
    assert isinstance(data, dict), f"В data не словарь, а {type(data)}: {data!r}"

    _, slice_data = json.loads(slice_book_facts)
    _, data_str = slice_data.split(":", maxsplit=1)
    data_book_facts: dict[str, Any]
    _, _, _, data_book_facts = json.loads(data_str)
    assert isinstance(
        data_book_facts, dict
    ), f"В data_book_facts не словарь, а {type(data_book_facts)}: {data_book_facts!r}"

    def deep_find(
        data: dict[str, Any] | list[Any],
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
    row: tuple[str, str, str | None, dict] | bool
    for row in data_children:
        if not row:
            continue

        item = row[3]
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

    chapters: int = -1
    characters: int = -1
    characters_str: str = "-"
    # NOTE: Example:
    """
    ...
        [
            "$",
            "div",
            null,
            {
                "className": "book-facts",
                "children": [
                    [
                        "$",
                        "$L33",
                        null,
                        {
                            "chapters": 1215,
                            "symbols": 11756790
                        }
                    ],
    """
    data_book_facts_children: list[tuple[str, str, Any, dict]] | None = deep_find(
        data_book_facts,
        has_key="className",
        has_value="book-facts",
        target_key="children",
    )
    assert data_book_facts_children, "Не найден класс book-facts в data_book_facts"
    assert isinstance(
        data_book_facts_children, list
    ), "Не найден список children в data_book_facts"
    row: tuple[str, str, str | None, dict] | bool
    for row in data_book_facts_children:
        if not row:
            continue

        item = row[3]

        assert isinstance(
            item, dict
        ), f"data_book_facts_children/children[]/item[3] is not dict: {item!r}"

        if "chapters" in item and "symbols" in item:
            chapters: int = item["chapters"]
            characters: int = item["symbols"]
            characters_str: str = str(characters)
            break

    return Ranobe(
        title=title,
        release_year=release_year,
        country=country,
        status=status,
        chapters=chapters,
        characters=characters,
        characters_str=characters_str,
        genres=all_genres,
        tags=all_tags,
        parser_version="v2",
    )


def get_ranobe_info(url: str) -> Ranobe:
    print(f"Load url: {url}")

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
    print(f"Genres: ({len(ranobe.genres)}): {ranobe.genres}")
    print(f"Tags: ({len(ranobe.tags)}): {ranobe.tags}")
    """
    Ranobe(title='Мир Бога и Дьявола', release_year=2013, country='Китай', status='Завершено', chapters=1215, characters=11756790, parser_version='v2')
    Genres: (13): ['Боевые искусства', 'Гарем', 'Драма', 'Зрелая тематика', 'Милитари', 'Научная фантастика', 'Приключение', 'Сэйнэн', 'Сюаньхуа', 'Трагедия', 'Фэнтези', 'Экшн', 'Эччи']
    Tags: (57): ['Антигерой', 'Апокалипсис', 'Армия', 'Артефакты', 'Безжалостный главный герой', 'Боги', 'Вампиры', 'Войны', 'Выживание', 'Гарем рабов', 'Генералы', 'Главный герой — мужчина', 'Горничные', 'Домашние дела', 'Драконы', 'Жертва изнасилования влюбляется в насильника', 'Звери', 'Звери-компаньоны', 'Злой протагонист', 'Зомби', 'Игра на выживание', 'Игровые элементы', 'Из слабого в сильного', 'Изнасилование', 'Искусственный интеллект', 'Каннибализм', 'Книги', 'Книги навыков', 'Контроль разума/сознания', 'Коррупция', 'Лидерство', 'Лоли', 'Магия', 'Множество реальностей', 'Монстры', 'Мутированные существа', 'Национализм', 'Не блещущий внешне главный герой', 'Недоразумения', 'Огнестрельное оружие', 'Питомцы', 'Полигамия', 'Прекрасная героиня', 'Проститутки', 'Рабы', 'Расизм', 'Решительный главный герой', 'Родословная', 'Секс рабы', 'Система уровней', 'Современность', 'Создание армии', 'Создание королевства', 'Трудолюбивый главный герой', 'Фарминг', 'Эволюция', 'Эгоистичный главный герой']
    """

    print("\n" + "-" * 100 + "\n")

    url = "https://ranobehub.org/ranobe/345-overgeared"
    ranobe = get_ranobe_info(url)
    print(ranobe)
    print(f"Genres: ({len(ranobe.genres)}): {ranobe.genres}")
    print(f"Tags: ({len(ranobe.tags)}): {ranobe.tags}")
    """
    Ranobe(title='Во всеоружии', release_year=2014, country='Корея', status='Завершено', chapters=2908, characters=27279603, parser_version='v2')
    Genres: (6): ['Гарем', 'Комедия', 'Приключение', 'Сэйнэн', 'Фэнтези', 'Экшн']
    Tags: (104): ['Ад', 'Алхимия', 'Ангелы', 'Армия', 'Артефакты', 'Артисты', 'Бедный главный герой', 'Беременность', 'Бессмертные', 'Бесстыдный главный герой', 'Боги', 'Богини', 'Божественные силы', 'Брак', 'Вампиры', 'Верные подчиненные', 'Виртуальная реальность', 'Воскрешение', 'Гильдии', 'Главный герой — мужчина', 'Глуповатый главный герой', 'Гриндинг', 'Дварфы', 'Дворяне', 'Демоны', 'Денежный долг', 'Дискриминация', 'Добыча денег одно из основных стремлений главного героя', 'Драконы', 'Души', 'Есть манхва-адаптация', 'Злые боги', 'Знаменитый главный герой', 'Игровая система рейтинга', 'Игровые элементы', 'Из грязи в князи', 'Из слабого в сильного', 'Изменения внешнего вида', 'Империи', 'Интриги и заговоры', 'Искусственный интеллект', 'Книги', 'Книги навыков', 'Копейщик', 'Королевства', 'Крафт', 'Кругосветное путешествие', 'Кузнец', 'Легенды', 'ММОРПГ (ЛитРПГ)', 'Магия', 'Метаморфы', 'Меч и магия', 'Мечник', 'Мифические звери', 'Младшие сестры', 'Монстры', 'Наивный главный герой', 'Наследование', 'Не блещущий внешне главный герой', 'Недооцененный главный герой', 'Недоразумения', 'Орки', 'Освоение навыков', 'Отношения учитель-ученик', 'Отношения хозяин-слуга', 'Отсутствие здравого смысла', 'Первая любовь', 'Первый раз', 'Питомцы', 'Повествование от нескольких лиц/Несколько точек зрения', 'Подземелья', 'Прекрасная героиня', 'Пропуск времени', 'Расизм', 'Романтический подсюжет ', 'Рост персонажа', 'Рыцари', 'Святые', 'Семь смертных грехов', 'Система уровней', 'Системный администратор', 'Скульпторы', 'Слабый главный герой', 'Смерть', 'Смерть близких', 'Современность', 'Создание артефактов', 'Создание королевства', 'Создание навыков', 'Соперники в любви', 'Стрелки', 'Стрельба из лука', 'Танцоры', 'Трудолюбивый главный герой', 'Убийцы', 'Убийцы драконов', 'Укротитель монстров', 'Уродливый главный герой', 'Фарминг', 'Футуристический сеттинг', 'Хозяин подземелий', 'Элементальная магия', 'Эльфы']
    """
