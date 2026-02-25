#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import os

from collections import defaultdict
from typing import NamedTuple
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests


class Boss(NamedTuple):
    name: str
    url: str


def get_bosses(url: str) -> dict[str, list[Boss]]:
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, "html.parser")

    bosses_by_category = defaultdict(list)

    category_name = None

    for tr in root.select("table.article-table > tr"):
        # Заголовок первым идет
        th = tr.select_one("th")
        if th:
            category_name = th.text.strip().upper()
            continue

        if not category_name:
            continue

        td_list = []

        for a in tr.select("td table a[href]"):
            name = a.get_text(strip=True)
            if not name:
                continue

            url = urljoin(rs.url, a["href"])
            boss = Boss(name, url)

            td_list.append(boss)

        bosses_by_category[category_name] += td_list

    return bosses_by_category


def print_bosses(url: str, bosses: dict[str, list[Boss]]) -> None:
    total = sum(len(i) for i in bosses.values())
    print(f"{url} ({total}):")

    for category, bosses in bosses.items():
        print(f"{category} ({len(bosses)}):")

        for i, boss in enumerate(bosses, 1):
            print(f'    {i}. "{boss.name}": {boss.url}')

        print()

    print()


def convert_bosses_to_only_name(bosses: dict[str, list[Boss]]) -> dict[str, list[str]]:
    bosses_only_name = dict()
    for category, bosses_list in bosses.items():
        bosses_only_name[category] = [boss.name for boss in bosses_list]

    return bosses_only_name


def export_to_json(file_name, bosses) -> None:
    dir_name = os.path.dirname(file_name)
    os.makedirs(dir_name, exist_ok=True)

    json.dump(
        bosses,
        open(file_name, "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
    )


def export_to_simple_text(file_name, bosses) -> None:
    dir_name = os.path.dirname(file_name)
    os.makedirs(dir_name, exist_ok=True)

    with open(file_name, "w", encoding="utf-8") as f:
        num = 0

        for category, bosses_list in bosses.items():
            num += 1
            if num > 1:
                f.write("\n")

            f.write(category + "\n")

            for boss in bosses_list:
                f.write(f"    {boss.name}\n")


if __name__ == "__main__":
    url = "https://demonssouls.fandom.com/ru/wiki/Боссы"
    bosses = get_bosses(url)
    print("Total bosses:", sum(len(i) for i in bosses.values()))
    # Total bosses: 21

    print()

    print_bosses(url, bosses)
    # https://demonssouls.fandom.com/ru/wiki/Боссы (21):
    # ОБЯЗАТЕЛЬНЫЕ БОССЫ (17):
    #     1. "Фаланга": https://demonssouls.fandom.com/ru/wiki/%D0%A4%D0%B0%D0%BB%D0%B0%D0%BD%D0%B3%D0%B0
    #     2. "Рыцарь башни": https://demonssouls.fandom.com/ru/wiki/%D0%A0%D1%8B%D1%86%D0%B0%D1%80%D1%8C_%D0%B1%D0%B0%D1%88%D0%BD%D0%B8
    #     3. "Пронзающий": https://demonssouls.fandom.com/ru/wiki/%D0%9F%D1%80%D0%BE%D0%BD%D0%B7%D0%B0%D1%8E%D1%89%D0%B8%D0%B9
    #     4. "Старый король Аллант": https://demonssouls.fandom.com/ru/wiki/%D0%A1%D1%82%D0%B0%D1%80%D1%8B%D0%B9_%D0%BA%D0%BE%D1%80%D0%BE%D0%BB%D1%8C_%D0%90%D0%BB%D0%BB%D0%B0%D0%BD%D1%82
    #     5. "Стальной паук": https://demonssouls.fandom.com/ru/wiki/%D0%A1%D1%82%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9_%D0%BF%D0%B0%D1%83%D0%BA
    #     6. "Огненный Соглядатай": https://demonssouls.fandom.com/ru/wiki/%D0%9E%D0%B3%D0%BD%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9_%D0%A1%D0%BE%D0%B3%D0%BB%D1%8F%D0%B4%D0%B0%D1%82%D0%B0%D0%B9
    #     7. "Бог драконов": https://demonssouls.fandom.com/ru/wiki/%D0%91%D0%BE%D0%B3_%D0%B4%D1%80%D0%B0%D0%BA%D0%BE%D0%BD%D0%BE%D0%B2
    #     8. "Ложный Идол": https://demonssouls.fandom.com/ru/wiki/%D0%9B%D0%BE%D0%B6%D0%BD%D1%8B%D0%B9_%D0%98%D0%B4%D0%BE%D0%BB
    #     9. "Людоед": https://demonssouls.fandom.com/ru/wiki/%D0%9B%D1%8E%D0%B4%D0%BE%D0%B5%D0%B4
    #     10. "Старый Монах": https://demonssouls.fandom.com/ru/wiki/%D0%A1%D1%82%D0%B0%D1%80%D1%8B%D0%B9_%D0%9C%D0%BE%D0%BD%D0%B0%D1%85
    #     11. "Судья": https://demonssouls.fandom.com/ru/wiki/%D0%A1%D1%83%D0%B4%D1%8C%D1%8F
    #     12. "Старый герой": https://demonssouls.fandom.com/ru/wiki/%D0%A1%D1%82%D0%B0%D1%80%D1%8B%D0%B9_%D0%B3%D0%B5%D1%80%D0%BE%D0%B9
    #     13. "Властитель Бурь (босс)": https://demonssouls.fandom.com/ru/wiki/%D0%92%D0%BB%D0%B0%D1%81%D1%82%D0%B8%D1%82%D0%B5%D0%BB%D1%8C_%D0%91%D1%83%D1%80%D1%8C_(%D0%B1%D0%BE%D1%81%D1%81)
    #     14. "Торговец пиявками": https://demonssouls.fandom.com/ru/wiki/%D0%A2%D0%BE%D1%80%D0%B3%D0%BE%D0%B2%D0%B5%D1%86_%D0%BF%D0%B8%D1%8F%D0%B2%D0%BA%D0%B0%D0%BC%D0%B8
    #     15. "Грязный Колосс": https://demonssouls.fandom.com/ru/wiki/%D0%93%D1%80%D1%8F%D0%B7%D0%BD%D1%8B%D0%B9_%D0%9A%D0%BE%D0%BB%D0%BE%D1%81%D1%81
    #     16. "Дева Астрея": https://demonssouls.fandom.com/ru/wiki/%D0%94%D0%B5%D0%B2%D0%B0_%D0%90%D1%81%D1%82%D1%80%D0%B5%D1%8F
    #     17. "Король Аллант": https://demonssouls.fandom.com/ru/wiki/%D0%9A%D0%BE%D1%80%D0%BE%D0%BB%D1%8C_%D0%90%D0%BB%D0%BB%D0%B0%D0%BD%D1%82
    #
    # ОПЦИОНАЛЬНЫЕ БОССЫ (4):
    #     1. "Авангард": https://demonssouls.fandom.com/ru/wiki/%D0%90%D0%B2%D0%B0%D0%BD%D0%B3%D0%B0%D1%80%D0%B4
    #     2. "Красный дракон": https://demonssouls.fandom.com/ru/wiki/%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D1%8B%D0%B9_%D0%B4%D1%80%D0%B0%D0%BA%D0%BE%D0%BD
    #     3. "Синий дракон": https://demonssouls.fandom.com/ru/wiki/%D0%A1%D0%B8%D0%BD%D0%B8%D0%B9_%D0%B4%D1%80%D0%B0%D0%BA%D0%BE%D0%BD
    #     4. "Первобытный демон": https://demonssouls.fandom.com/ru/wiki/%D0%9F%D0%B5%D1%80%D0%B2%D0%BE%D0%B1%D1%8B%D1%82%D0%BD%D1%8B%D0%B9_%D0%B4%D0%B5%D0%BC%D0%BE%D0%BD

    export_to_json("dumps/bosses.json", bosses)
    export_to_json("dumps/bosses__only_name.json", convert_bosses_to_only_name(bosses))
    export_to_simple_text("dumps/bosses__only_name.txt", bosses)
