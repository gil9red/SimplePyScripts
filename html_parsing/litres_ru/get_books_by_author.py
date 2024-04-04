#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from dataclasses import dataclass

import requests


@dataclass
class Book:
    name: str
    series: str
    seq: int = 0

    def get_full_name(self) -> str:
        seq_str = f"{self.seq}. " if self.seq else ""
        return f"[{self.series}] {seq_str}{self.name}"


session = requests.Session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"


URL_API_PATTERN: str = (
    "https://api.litres.ru/foundation/api/authors/{name}/arts"
    "?art_groups=1&limit=50&o=series&show_unavailable=true"
)


def get_books(url: str) -> list[Book]:
    def _process_title(text: str) -> str:
        return text.replace("\xa0", " ")

    m = re.search(r"/author/(.+?)/", url)
    if not m:
        raise Exception(f"Не получилось найти имя автора из ссылки {url}")

    name = m.group(1)

    # TODO: Поддержка загрузки всех страниц [payload][pagination][next_page]
    url: str = URL_API_PATTERN.format(name=name)

    rs = session.get(url)
    rs.raise_for_status()

    books: list[Book] = []
    for book in rs.json()["payload"]["data"]:
        name: str = _process_title(book["title"])

        if book["series"]:
            series_name: str = _process_title(book["series"][0]["name"])
            seq: int = book["series"][0]["art_order"]
        else:
            series_name: str = "Без серии"
            seq: int = 0

        books.append(
            Book(
                name=name,
                series=series_name,
                seq=seq,
            )
        )

    assert books, "Вернулся пустой список книг"
    return books


if __name__ == "__main__":
    url = "https://www.litres.ru/author/vitaliy-zykov/"
    books = get_books(url)
    print(f"Книги ({len(books)}):")
    for book in books:
        print(f"{book.get_full_name()!r} <-> {book}")
    """
    Книги (19):
    '[Дорога домой] 1. Безымянный раб' <-> Book(name='Безымянный раб', series='Дорога домой', seq=1)
    '[Дорога домой] 2. Наемник Его Величества' <-> Book(name='Наемник Его Величества', series='Дорога домой', seq=2)
    '[Дорога домой] 3. Под знаменем пророчества' <-> Book(name='Под знаменем пророчества', series='Дорога домой', seq=3)
    '[Дорога домой] 4. Владыка Сардуора' <-> Book(name='Владыка Сардуора', series='Дорога домой', seq=4)
    '[Дорога домой] 5. Власть силы. Том 2. Когда враги становятся друзьями' <-> Book(name='Власть силы. Том 2. Когда враги становятся друзьями', series='Дорога домой', seq=5)
    '[Дорога домой] 5. Власть силы. Том 1. Война на пороге' <-> Book(name='Власть силы. Том 1. Война на пороге', series='Дорога домой', seq=5)
    '[Дорога домой] 6. Великие Спящие. Том 2. Свет против Света' <-> Book(name='Великие Спящие. Том 2. Свет против Света', series='Дорога домой', seq=6)
    '[Дорога домой] 6. Великие Спящие. Том 1. Тьма против Тьмы' <-> Book(name='Великие Спящие. Том 1. Тьма против Тьмы', series='Дорога домой', seq=6)
    '[Война за выживание] 1. Конклав Бессмертных. В краю далеком' <-> Book(name='Конклав Бессмертных. В краю далеком', series='Война за выживание', seq=1)
    '[Война за выживание] 2. Конклав Бессмертных. Проба сил' <-> Book(name='Конклав Бессмертных. Проба сил', series='Война за выживание', seq=2)
    '[Война за выживание] 3. Во имя потерянных душ' <-> Book(name='Во имя потерянных душ', series='Война за выживание', seq=3)
    '[Мир бесчисленных островов] 1. Малк. Когда у тебя нет цели' <-> Book(name='Малк. Когда у тебя нет цели', series='Мир бесчисленных островов', seq=1)
    '[Мир бесчисленных островов] 2. Малк. И когда ты её нашёл' <-> Book(name='Малк. И когда ты её нашёл', series='Мир бесчисленных островов', seq=2)
    '[Мир бесчисленных островов] 3. Школа пепла' <-> Book(name='Школа пепла', series='Мир бесчисленных островов', seq=3)
    '[Мир бесчисленных островов] 4. Обратная сторона Власти' <-> Book(name='Обратная сторона Власти', series='Мир бесчисленных островов', seq=4)
    '[Мир бесчисленных островов] 5. Ученик своего учителя. Ветер свободы' <-> Book(name='Ученик своего учителя. Ветер свободы', series='Мир бесчисленных островов', seq=5)
    '[Мир бесчисленных островов] 6. Ученик своего учителя. Родная гавань' <-> Book(name='Ученик своего учителя. Родная гавань', series='Мир бесчисленных островов', seq=6)
    '[Без серии] Флорист' <-> Book(name='Флорист', series='Без серии', seq=0)
    '[Без серии] Наследство Братства Сумерек' <-> Book(name='Наследство Братства Сумерек', series='Без серии', seq=0)
    """
