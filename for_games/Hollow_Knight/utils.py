#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from collections import OrderedDict
from typing import NamedTuple
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests


class Boss(NamedTuple):
    name: str
    url: str


def get_bosses() -> dict[str, list[Boss]]:
    url = "https://hollowknight.fandom.com/ru/wiki/Боссы"

    rs = requests.get(url)
    root = BeautifulSoup(rs.content, "html.parser")

    bosses_by_category = dict()

    for h2 in root.select("h2"):
        category = h2.select_one(".mw-headline")
        if not category:
            continue

        table = h2.find_next_sibling("table")
        if not table:
            continue

        category_name = category.get_text(strip=True)
        bosses = []

        for item in table.select("td > b > a"):
            boss_url = urljoin(rs.url, item["href"])
            boss_name = item.get_text(strip=True)

            boss = Boss(boss_name, boss_url)
            bosses.append(boss)

        bosses_by_category[category_name] = bosses

    return bosses_by_category


def convert_bosses_to_only_name(bosses: dict[str, list[Boss]]) -> dict[str, list[str]]:
    bosses_only_name = OrderedDict()
    for category, bosses_list in bosses.items():
        bosses_only_name[category] = [boss.name for boss in bosses_list]

    return bosses_only_name


if __name__ == "__main__":
    bosses_by_category = get_bosses()
    for category, bosses in bosses_by_category.items():
        print(category)
        for boss in bosses:
            print(f'    "{boss.name}": {boss.url}')
        print()
    # ...

    print()

    bosses_by_category = convert_bosses_to_only_name(bosses_by_category)
    for category, boss_names in bosses_by_category.items():
        print(category)
        for name in boss_names:
            print("    " + name)
        print()
    """
    Боссы
        Матка Жужж
        Ложный Рыцарь/Сломленный чемпион
        Задумчивый чревень
        Закруглан
        Воин душ
        Король мстекрылов
        Разбитый Сосуд/Потерянный собрат
        Кристаллический страж
        Навозный защитник
        Тремоматка
        Божья укротительница
        Полый рыцарь
        Хорнет
        Лорды богомолов
        Носк
        Мастер душ/Душегуб
        Коллекционер
        Лучезарность
        Предавший лорд
        Ууму
        Рыцарь-хранитель
        Серый принц Зот
        Белый защитник
        Гримм
        Король кошмара
        Рыцарь Улья
        Мастера гвоздя Оро и Мато
        Мастер кисти Шео
        Великий гуру гвоздей Слай
        Боевые сёстры
        Крылатый Носк
        Чистый Сосуд
        Всевышняя Лучезарность
    
    Воины грёз
        Старейшина Ху
        Гальен
        Горб
        Маркот
        Марму
        Незрячая
        Ксеро
    """
