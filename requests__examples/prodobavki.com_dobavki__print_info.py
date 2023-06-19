#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import textwrap

import requests
from bs4 import BeautifulSoup


def print_info(url):
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, "lxml")

    # Пример:
    # E200 — Сорбиновая кислота
    print(root.select_one("#mcenter > .path > .path3 > h1").text)
    print()

    # Пример:
    # Описание пищевой добавки
    print(root.select_one("#info_content > h2").text)

    # Пример:
    # Сорбиновая кислота (Е-200) - пищевая добавка-консервант. Сорбиновая
    # кислота обладает эффективным антимикробным действием – подавляет рост
    # большинстве микроорганизмов, особенно дрожжевых грибков и плесеней.
    # Содержится в соке рябине рода Sorbus.
    print(textwrap.fill(root.select_one("#info_content > h2 ~ p").text))
    print()

    # Пример:
    # Законы и документы о пищевой добавке:
    # Разрешающие применение — 4
    # Упоминаний о добавке— 6
    print("\n".join(tag.text for tag in root.select("#legacy_badge > .legacydocs > *")))
    print()

    # Пример:
    # Законы и документы о пищевой добавке:
    # Разрешающие применение — 4
    # Упоминаний о добавке— 6
    # Применение добавки по странам:
    # Россия — разрешена
    # Украина — разрешена
    # Беларусь — разрешена
    # Евросоюз — разрешена
    # Канада — разрешена
    # США — разрешена
    print(
        "\n".join(
            tag.text for tag in root.select("#legacy_badge > div > .legacydocs > *")
        )
    )


if __name__ == "__main__":
    print_info("https://prodobavki.com/dobavki/E200.html")
    print("\n")

    print_info("https://prodobavki.com/dobavki/E220.html")
