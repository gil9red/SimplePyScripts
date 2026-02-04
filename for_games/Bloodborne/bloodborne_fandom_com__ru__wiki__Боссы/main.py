#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json

from collections import defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests


@dataclass
class Boss:
    name: str
    url: str


URL: str = "https://bloodborne.fandom.com/ru/wiki/Боссы"


def get_bosses() -> dict[str, list[Boss]]:
    rs = requests.get(URL)
    rs.raise_for_status()

    soup = BeautifulSoup(rs.content, "html.parser")

    bosses_by_category: dict[str, list[Boss]] = defaultdict(list)
    category_name: str | None = None

    for tr in soup.select("table.article-table tr"):
        # Заголовок первым идет
        th = tr.select_one("th")
        if th:
            category_name = th.text.strip().upper()
            continue

        if not category_name:
            continue

        bosses_by_category[category_name] += [
            Boss(
                name=a["title"],
                url=urljoin(rs.url, a["href"]),
            )
            for a in tr.select("td > figure > a[href][title]")
        ]

    return bosses_by_category


def print_bosses(bosses: dict[str, list[Boss]]):
    total = sum(len(i) for i in bosses.values())
    print(f"Боссы ({total}):")

    for category, bosses in bosses.items():
        print(f"{category} ({len(bosses)}):")

        for i, boss in enumerate(bosses, 1):
            print(f'    {i}. "{boss.name}": {boss.url}')

        print()


def convert_bosses_to_only_name(bosses: dict[str, list[Boss]]) -> dict[str, list[str]]:
    bosses_only_name = dict()
    for category, bosses_list in bosses.items():
        bosses_only_name[category] = [boss.name for boss in bosses_list]

    return bosses_only_name


def export_to_json(file_name: Path, bosses: dict[str, list[Boss | str]]):
    file_name.parent.mkdir(parents=True, exist_ok=True)

    json.dump(
        bosses,
        open(file_name, "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
        default=asdict,
    )


def export_to_simple_text(file_name, bosses: dict[str, list[Boss]]):
    file_name.parent.mkdir(parents=True, exist_ok=True)

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
    DIR: Path = Path(__file__).resolve().parent

    bosses: dict[str, list[Boss]] = get_bosses()
    print("Всего боссов:", sum(len(i) for i in bosses.values()))
    # Всего боссов: 44

    print()

    print_bosses(bosses)
    """
    Боссы (44):
    ОСНОВНАЯ ИГРА. ОБЯЗАТЕЛЬНЫЕ БОССЫ (7):
        1. "Отец Гаскойн": https://bloodborne.fandom.com/ru/wiki/%D0%9E%D1%82%D0%B5%D1%86_%D0%93%D0%B0%D1%81%D0%BA%D0%BE%D0%B9%D0%BD
        2. "Викарий Амелия": https://bloodborne.fandom.com/ru/wiki/%D0%92%D0%B8%D0%BA%D0%B0%D1%80%D0%B8%D0%B9_%D0%90%D0%BC%D0%B5%D0%BB%D0%B8%D1%8F
        3. "Тень Ярнама": https://bloodborne.fandom.com/ru/wiki/%D0%A2%D0%B5%D0%BD%D1%8C_%D0%AF%D1%80%D0%BD%D0%B0%D0%BC%D0%B0
        4. "Ром, праздный паук": https://bloodborne.fandom.com/ru/wiki/%D0%A0%D0%BE%D0%BC,_%D0%BF%D1%80%D0%B0%D0%B7%D0%B4%D0%BD%D1%8B%D0%B9_%D0%BF%D0%B0%D1%83%D0%BA
        5. "Возродившийся": https://bloodborne.fandom.com/ru/wiki/%D0%92%D0%BE%D0%B7%D1%80%D0%BE%D0%B4%D0%B8%D0%B2%D1%88%D0%B8%D0%B9%D1%81%D1%8F
        6. "Миколаш, Хозяин кошмара": https://bloodborne.fandom.com/ru/wiki/%D0%9C%D0%B8%D0%BA%D0%BE%D0%BB%D0%B0%D1%88,_%D0%A5%D0%BE%D0%B7%D1%8F%D0%B8%D0%BD_%D0%BA%D0%BE%D1%88%D0%BC%D0%B0%D1%80%D0%B0
        7. "Кормилица Мерго": https://bloodborne.fandom.com/ru/wiki/%D0%9A%D0%BE%D1%80%D0%BC%D0%B8%D0%BB%D0%B8%D1%86%D0%B0_%D0%9C%D0%B5%D1%80%D0%B3%D0%BE
    
    ОСНОВНАЯ ИГРА. ОПЦИОНАЛЬНЫЕ БОССЫ (10):
        1. "Церковное Чудовище": https://bloodborne.fandom.com/ru/wiki/%D0%A6%D0%B5%D1%80%D0%BA%D0%BE%D0%B2%D0%BD%D0%BE%D0%B5_%D0%A7%D1%83%D0%B4%D0%BE%D0%B2%D0%B8%D1%89%D0%B5
        2. "Посланник Небес": https://bloodborne.fandom.com/ru/wiki/%D0%9F%D0%BE%D1%81%D0%BB%D0%B0%D0%BD%D0%BD%D0%B8%D0%BA_%D0%9D%D0%B5%D0%B1%D0%B5%D1%81
        3. "Ибраитас, дочь Космоса": https://bloodborne.fandom.com/ru/wiki/%D0%98%D0%B1%D1%80%D0%B0%D0%B8%D1%82%D0%B0%D1%81,_%D0%B4%D0%BE%D1%87%D1%8C_%D0%9A%D0%BE%D1%81%D0%BC%D0%BE%D1%81%D0%B0
        4. "Чудовище-кровоглот": https://bloodborne.fandom.com/ru/wiki/%D0%A7%D1%83%D0%B4%D0%BE%D0%B2%D0%B8%D1%89%D0%B5-%D0%BA%D1%80%D0%BE%D0%B2%D0%BE%D0%B3%D0%BB%D0%BE%D1%82
        5. "Черное чудовище Паарл": https://bloodborne.fandom.com/ru/wiki/%D0%A7%D0%B5%D1%80%D0%BD%D0%BE%D0%B5_%D1%87%D1%83%D0%B4%D0%BE%D0%B2%D0%B8%D1%89%D0%B5_%D0%9F%D0%B0%D0%B0%D1%80%D0%BB
        6. "Ведьма Хемвика": https://bloodborne.fandom.com/ru/wiki/%D0%92%D0%B5%D0%B4%D1%8C%D0%BC%D0%B0_%D0%A5%D0%B5%D0%BC%D0%B2%D0%B8%D0%BA%D0%B0
        7. "Мученик Логариус": https://bloodborne.fandom.com/ru/wiki/%D0%9C%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%BA_%D0%9B%D0%BE%D0%B3%D0%B0%D1%80%D0%B8%D1%83%D1%81
        8. "Амигдала": https://bloodborne.fandom.com/ru/wiki/%D0%90%D0%BC%D0%B8%D0%B3%D0%B4%D0%B0%D0%BB%D0%B0
        9. "Герман, первый охотник": https://bloodborne.fandom.com/ru/wiki/%D0%93%D0%B5%D1%80%D0%BC%D0%B0%D0%BD,_%D0%BF%D0%B5%D1%80%D0%B2%D1%8B%D0%B9_%D0%BE%D1%85%D0%BE%D1%82%D0%BD%D0%B8%D0%BA
        10. "Присутствие луны": https://bloodborne.fandom.com/ru/wiki/%D0%9F%D1%80%D0%B8%D1%81%D1%83%D1%82%D1%81%D1%82%D0%B2%D0%B8%D0%B5_%D0%BB%D1%83%D0%BD%D1%8B
    
    ДОПОЛНЕНИЕ THE OLD HUNTERS (5):
        1. "Людвиг": https://bloodborne.fandom.com/ru/wiki/%D0%9B%D1%8E%D0%B4%D0%B2%D0%B8%D0%B3
        2. "Лоуренс, первый викарий": https://bloodborne.fandom.com/ru/wiki/%D0%9B%D0%BE%D1%83%D1%80%D0%B5%D0%BD%D1%81,_%D0%BF%D0%B5%D1%80%D0%B2%D1%8B%D0%B9_%D0%B2%D0%B8%D0%BA%D0%B0%D1%80%D0%B8%D0%B9
        3. "Живые неудачи": https://bloodborne.fandom.com/ru/wiki/%D0%96%D0%B8%D0%B2%D1%8B%D0%B5_%D0%BD%D0%B5%D1%83%D0%B4%D0%B0%D1%87%D0%B8
        4. "Леди Мария из Астральной часовой башни": https://bloodborne.fandom.com/ru/wiki/%D0%9B%D0%B5%D0%B4%D0%B8_%D0%9C%D0%B0%D1%80%D0%B8%D1%8F_%D0%B8%D0%B7_%D0%90%D1%81%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9_%D1%87%D0%B0%D1%81%D0%BE%D0%B2%D0%BE%D0%B9_%D0%B1%D0%B0%D1%88%D0%BD%D0%B8
        5. "Сирота Кос": https://bloodborne.fandom.com/ru/wiki/%D0%A1%D0%B8%D1%80%D0%BE%D1%82%D0%B0_%D0%9A%D0%BE%D1%81
    
    ОБЛАСТЬ ПТУМЕРУ (10):
        1. "Мертвый гигант": https://bloodborne.fandom.com/ru/wiki/%D0%9C%D0%B5%D1%80%D1%82%D0%B2%D1%8B%D0%B9_%D0%B3%D0%B8%D0%B3%D0%B0%D0%BD%D1%82
        2. "Беспощадные Хранители": https://bloodborne.fandom.com/ru/wiki/%D0%91%D0%B5%D1%81%D0%BF%D0%BE%D1%89%D0%B0%D0%B4%D0%BD%D1%8B%D0%B5_%D0%A5%D1%80%D0%B0%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D0%B8
        3. "Сторожевой пес Древних Богов": https://bloodborne.fandom.com/ru/wiki/%D0%A1%D1%82%D0%BE%D1%80%D0%BE%D0%B6%D0%B5%D0%B2%D0%BE%D0%B9_%D0%BF%D0%B5%D1%81_%D0%94%D1%80%D0%B5%D0%B2%D0%BD%D0%B8%D1%85_%D0%91%D0%BE%D0%B3%D0%BE%D0%B2
        4. "Душа, одержимая чудовищем": https://bloodborne.fandom.com/ru/wiki/%D0%94%D1%83%D1%88%D0%B0,_%D0%BE%D0%B4%D0%B5%D1%80%D0%B6%D0%B8%D0%BC%D0%B0%D1%8F_%D1%87%D1%83%D0%B4%D0%BE%D0%B2%D0%B8%D1%89%D0%B5%D0%BC
        5. "Хранитель Древних Богов": https://bloodborne.fandom.com/ru/wiki/%D0%A5%D1%80%D0%B0%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8C_%D0%94%D1%80%D0%B5%D0%B2%D0%BD%D0%B8%D1%85_%D0%91%D0%BE%D0%B3%D0%BE%D0%B2
        6. "Потомок птумериан": https://bloodborne.fandom.com/ru/wiki/%D0%9F%D0%BE%D1%82%D0%BE%D0%BC%D0%BE%D0%BA_%D0%BF%D1%82%D1%83%D0%BC%D0%B5%D1%80%D0%B8%D0%B0%D0%BD
        7. "Ром, праздный паук": https://bloodborne.fandom.com/ru/wiki/%D0%A0%D0%BE%D0%BC,_%D0%BF%D1%80%D0%B0%D0%B7%D0%B4%D0%BD%D1%8B%D0%B9_%D0%BF%D0%B0%D1%83%D0%BA
        8. "Чудовище-кровопуск": https://bloodborne.fandom.com/ru/wiki/%D0%A7%D1%83%D0%B4%D0%BE%D0%B2%D0%B8%D1%89%D0%B5-%D0%BA%D1%80%D0%BE%D0%B2%D0%BE%D0%BF%D1%83%D1%81%D0%BA
        9. "Амигдала": https://bloodborne.fandom.com/ru/wiki/%D0%90%D0%BC%D0%B8%D0%B3%D0%B4%D0%B0%D0%BB%D0%B0
        10. "Ярнам, Птумерианская королева": https://bloodborne.fandom.com/ru/wiki/%D0%AF%D1%80%D0%BD%D0%B0%D0%BC,_%D0%9F%D1%82%D1%83%D0%BC%D0%B5%D1%80%D0%B8%D0%B0%D0%BD%D1%81%D0%BA%D0%B0%D1%8F_%D0%BA%D0%BE%D1%80%D0%BE%D0%BB%D0%B5%D0%B2%D0%B0
    
    ОБЛАСТЬ ДАЛЬНИХ ГРОБНИЦ (5):
        1. "Вепрь-людоед": https://bloodborne.fandom.com/ru/wiki/%D0%92%D0%B5%D0%BF%D1%80%D1%8C-%D0%BB%D1%8E%D0%B4%D0%BE%D0%B5%D0%B4
        2. "Чудовище-кровоглот": https://bloodborne.fandom.com/ru/wiki/%D0%A7%D1%83%D0%B4%D0%BE%D0%B2%D0%B8%D1%89%D0%B5-%D0%BA%D1%80%D0%BE%D0%B2%D0%BE%D0%B3%D0%BB%D0%BE%D1%82
        3. "Мозгосос": https://bloodborne.fandom.com/ru/wiki/%D0%9C%D0%BE%D0%B7%D0%B3%D0%BE%D1%81%D0%BE%D1%81
        4. "Забытый безумец": https://bloodborne.fandom.com/ru/wiki/%D0%97%D0%B0%D0%B1%D1%8B%D1%82%D1%8B%D0%B9_%D0%B1%D0%B5%D0%B7%D1%83%D0%BC%D0%B5%D1%86
        5. "Птумерианский Старейшина": https://bloodborne.fandom.com/ru/wiki/%D0%9F%D1%82%D1%83%D0%BC%D0%B5%D1%80%D0%B8%D0%B0%D0%BD%D1%81%D0%BA%D0%B8%D0%B9_%D0%A1%D1%82%D0%B0%D1%80%D0%B5%D0%B9%D1%88%D0%B8%D0%BD%D0%B0
    
    ОБЛАСТЬ ЛОРАНА (4):
        1. "Чудовище-кровоглот": https://bloodborne.fandom.com/ru/wiki/%D0%A7%D1%83%D0%B4%D0%BE%D0%B2%D0%B8%D1%89%D0%B5-%D0%BA%D1%80%D0%BE%D0%B2%D0%BE%D0%B3%D0%BB%D0%BE%D1%82
        2. "Отвратительное чудовище": https://bloodborne.fandom.com/ru/wiki/%D0%9E%D1%82%D0%B2%D1%80%D0%B0%D1%82%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D0%B5_%D1%87%D1%83%D0%B4%D0%BE%D0%B2%D0%B8%D1%89%D0%B5
        3. "Серебряное чудовище Лорана": https://bloodborne.fandom.com/ru/wiki/%D0%A1%D0%B5%D1%80%D0%B5%D0%B1%D1%80%D1%8F%D0%BD%D0%BE%D0%B5_%D1%87%D1%83%D0%B4%D0%BE%D0%B2%D0%B8%D1%89%D0%B5_%D0%9B%D0%BE%D1%80%D0%B0%D0%BD%D0%B0
        4. "Черное чудовище Паарл": https://bloodborne.fandom.com/ru/wiki/%D0%A7%D0%B5%D1%80%D0%BD%D0%BE%D0%B5_%D1%87%D1%83%D0%B4%D0%BE%D0%B2%D0%B8%D1%89%D0%B5_%D0%9F%D0%B0%D0%B0%D1%80%D0%BB
    
    ОБЛАСТЬ ИСЗА (3):
        1. "Мозгосос": https://bloodborne.fandom.com/ru/wiki/%D0%9C%D0%BE%D0%B7%D0%B3%D0%BE%D1%81%D0%BE%D1%81
        2. "Посланник Небес": https://bloodborne.fandom.com/ru/wiki/%D0%9F%D0%BE%D1%81%D0%BB%D0%B0%D0%BD%D0%BD%D0%B8%D0%BA_%D0%9D%D0%B5%D0%B1%D0%B5%D1%81
        3. "Ибраитас, дочь Космоса": https://bloodborne.fandom.com/ru/wiki/%D0%98%D0%B1%D1%80%D0%B0%D0%B8%D1%82%D0%B0%D1%81,_%D0%B4%D0%BE%D1%87%D1%8C_%D0%9A%D0%BE%D1%81%D0%BC%D0%BE%D1%81%D0%B0

    """

    export_to_json(DIR / "dumps/bosses.json", bosses)
    export_to_json(
        DIR / "dumps/bosses__only_name.json", convert_bosses_to_only_name(bosses)
    )
    export_to_simple_text(DIR / "dumps/bosses__only_name.txt", bosses)
