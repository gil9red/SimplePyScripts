#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from bs4 import BeautifulSoup
from common import session


def get_notes(url: str) -> list[str]:
    rs = session.get(url)
    rs.raise_for_status()

    items = []

    soup = BeautifulSoup(rs.content, "html.parser")

    # NOTE: Example
    # <ol class="references">
    #     <li id="190cite_note-34548627613">
    #         <a href="#190cite_ref-34548627613">↑</a> Автор тут допустил небольшую ошибку. Циклотетраметилентетранитрамин ещё называют октогеном, но не СL-20. СL-20 будет «гексанитрогексаазаизовюрцитан», он более эффективен и стоит 1300 долларов за килограмм, октоген же — 100 долларов за килограмм.
    #     </li>
    # </ol>
    for li_el in soup.find_all("li", id=re.compile(".*cite_note.*")):
        li_el.a.decompose()
        items.append(
            li_el.get_text(strip=True)
        )

    return items


if __name__ == "__main__":
    url = "https://ranobehub.org/ranobe/19/17/4"
    notes = get_notes(url)
    print(f"Notes ({len(notes)}):")
    for note in notes:
        print(repr(note))
    """
    Notes (3):
    'Автор тут допустил небольшую ошибку. Циклотетраметилентетранитрамин ещё называют октогеном, но не СL-20. СL-20 будет «гексанитрогексаазаизовюрцитан», он более эффективен и стоит 1300 долларов за килограмм, октоген же — 100 долларов за килограмм.'
    'В предыдущих томах её фамилия была Баранс.'
    'Канопус: звезда южного полушария, вторая по яркости после Сириуса.'
    """
    print()

    url = "https://ranobehub.org/ranobe/19/21/2"
    notes = get_notes(url)
    print(f"Notes ({len(notes)}):")
    for note in notes:
        print(repr(note))
