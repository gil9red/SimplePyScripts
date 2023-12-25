#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


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


def get_books(url: str) -> list[Book]:
    rs = session.get(url)

    soup = BeautifulSoup(rs.content, "html.parser")

    # Список серии книг
    letter_els = soup.select(".person-page-list__content_sequence > div.letter_icon")
    assert letter_els, "Не удалось найти список серий!"

    all_books: list[Book] = []

    for div_el in letter_els:
        series_name = div_el.get_text(strip=True).replace("\xa0", " ")

        arts_by_letter = div_el.find_next_sibling(
            "div", attrs={"class": "arts_by_letter"}
        )
        assert (
            arts_by_letter
        ), f"Не удалось найти тег с списком книг (серия {series_name!r})"

        book_els = arts_by_letter.select(".arts_by_alphabet_item")
        assert book_els, f"Не удалось найти список книг (серия {series_name!r})"

        books: list[Book] = []
        for el in book_els:
            # Оставляем только текстовые книги, аудио не нужны
            if not el.select_one(".format-icons__block .text"):
                continue

            name_el = el.select_one("a.art_name_link")
            assert name_el, f"Не удалось найти название книги (серия {series_name!r})"

            name = name_el["title"].replace("\xa0", " ")

            seq_el = el.select_one(".art_name_link_seq")
            if seq_el:
                seq: int = int(
                    "".join(c for c in seq_el.get_text(strip=True) if c.isdigit())
                )
            else:
                seq = 0

            books.append(
                Book(
                    name=name,
                    series=series_name,
                    seq=seq,
                )
            )

        assert books, f"Вернулся пустой список книг (серия {series_name!r})"
        all_books += books

    assert all_books, "Вернулся пустой список книг"
    return all_books


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
