#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
import sys
from typing import Union, Dict, List, Tuple
from pathlib import Path

DIR = Path(__file__).resolve().parent

sys.path.append(str(DIR.parent))
sys.path.append(str(DIR.parent.parent))
sys.path.append(str(DIR.parent.parent.parent))

from config import URL_DS1, URL_DS2, URL_DS3
from utils import Boss, get_bosses

from ascii_table__simple_pretty__format import print_pretty_table


def only_digits(text: Union[str, int], do_sum=None) -> int:
    if not isinstance(text, str):
        return text

    if isinstance(do_sum, str):
        return sum(only_digits(x) for x in text.split(do_sum))

    return int(re.sub(r'\D', '', text))


def get_health(boss: Boss, items: Dict[str, List[str]]) -> int:
    health_items = items['Здоровье']

    boss_name = boss.name.lower()

    if boss_name == 'горгулья':
        return only_digits(health_items[0], do_sum='+')

    if boss_name == 'орнштейн и смоуг':
        return only_digits(health_items[1].split('&')[0], do_sum='/')

    # 3x 2,330
    if boss_name == 'стражи руин':
        h = health_items[0].split(' ')[-1]
        return 3 * only_digits(h)

    if boss_name in ['нагой сит', 'присцилла полукровка', 'черный дракон каламит']:
        return only_digits(health_items[1], do_sum='/')

    if boss_name == 'страж святилища':
        parts = health_items[1].split('/')
        return only_digits(parts[0]) + only_digits(parts[2])

    if boss_name == 'алчный демон':
        return only_digits(health_items[1])

    if boss_name in ['преследователь', 'знаток кристальных чар']:
        return only_digits(health_items[2])

    if boss_name == 'гибкий часовой':
        return only_digits(health_items[3])

    if 'заллен' in boss_name and 'луд' in boss_name:
        return only_digits(health_items[0], do_sum='/')

    if boss_name == 'душа пепла':
        first_idx = health_items.index('Первая фаза:')
        second_idx = health_items.index('Вторая Фаза:')
        return (
            only_digits(health_items[first_idx + 1])
            + only_digits(health_items[second_idx + 1])
        )

    if boss_name == 'два драконьих всадника':
        first_idx = health_items.index('Лучник:')
        second_idx = health_items.index('Воин:')
        return (
            only_digits(health_items[first_idx + 1])
            + only_digits(health_items[second_idx + 1])
        )

    if boss_name == 'защитник трона и смотритель трона':
        first_idx = health_items.index('Защитник:')
        second_idx = health_items.index('Смотритель:')
        return (
            only_digits(health_items[first_idx + 1])
            + only_digits(health_items[second_idx + 1])
        )

    if boss_name == 'копье церкви':
        return only_digits(health_items[2])

    if boss_name == 'хранители бездны':
        first_idx = health_items.index('Первая Фаза')
        second_idx = health_items.index('Вторая Фаза')
        return (
            only_digits(health_items[first_idx + 2])
            + only_digits(health_items[second_idx + 2])
        )

    if boss_name == 'лотрик, младший принц и лориан, старший принц':
        first_idx = health_items.index('Первая Фаза')
        second_idx = health_items.index('Вторая Фаза')
        lothric_idx = health_items.index('Лотрик')
        return (
            only_digits(health_items[first_idx + 2])
            + only_digits(health_items[second_idx + 2])
            + only_digits(health_items[lothric_idx + 1])
        )

    if boss_name == 'странствующий маг и прихожане':
        first_idx = health_items.index('Странствующий маг:')
        second_idx = health_items.index('Жрец:')
        third_idx = health_items.index('Полый проситель:')
        return (
            only_digits(health_items[first_idx + 1])
            + only_digits(health_items[second_idx + 1])
            + only_digits(health_items[third_idx + 1])
        )

    if boss_name == 'повелители скелетов':
        first_idx = health_items.index('Повелитель-воин:')
        second_idx = health_items.index('Повелитель-маг:')
        third_idx = health_items.index('Повелитель-жнец:')
        return (
            only_digits(health_items[first_idx + 1])
            + only_digits(health_items[second_idx + 1])
            + only_digits(health_items[third_idx + 1])
        )

    if boss_name == 'варг, церах и разорительница гробниц':
        first_idx = health_items.index('Скорбящая разорительница гробниц:')
        second_idx = health_items.index('Древний солдат Варг:')
        third_idx = health_items.index('Старый исследователь Церах:')
        return (
            only_digits(health_items[first_idx + 1])
            + only_digits(health_items[second_idx + 1])
            + only_digits(health_items[third_idx + 1])
        )

    if boss_name == 'безымянный король':
        first_idx = health_items.index('Повелитель Шторма')
        second_idx = health_items.index('Безымянный Король')
        return (
            only_digits(health_items[first_idx + 2])
            + only_digits(health_items[second_idx + 2])
        )

    if boss_name == 'хранитель могилы чемпиона и великий волк':
        first_idx = health_items.index('Хранитель')
        second_idx = health_items.index('Великий волк')
        return (
            only_digits(health_items[first_idx + 2])
            + only_digits(health_items[second_idx + 2])
        )

    if boss_name == 'отец ариандель и сестра фриде':
        first_idx = health_items.index('Сестра Фриде')
        second_idx = health_items.index('Отец Ариандель и сестра Фриде')
        third_idx = health_items.index('Черное пламя Фриде')
        return (
            only_digits(health_items[first_idx + 2])
            + only_digits(health_items[second_idx + 2])
            + only_digits(health_items[third_idx + 2])
        )

    if boss_name == 'демон-принц':
        first_idx = health_items.index('Демон в агонии/Демон из глубин')
        second_idx = health_items.index('Демон-принц')
        return (
            only_digits(health_items[first_idx + 2], do_sum='/')
            + only_digits(health_items[second_idx + 2])
        )

    health_value = health_items[0]
    return only_digits(health_value)


def get_souls(boss: Boss, items: Dict[str, List[str]]) -> int:
    souls_items = items['Души']

    boss_name = boss.name.lower()

    if boss_name == 'страж святилища':
        return only_digits(souls_items[1].split('/')[1])

    if boss_name in ['преследователь', 'знаток кристальных чар']:
        return only_digits(souls_items[2])

    if boss_name == 'гибкий часовой':
        return only_digits(souls_items[3])

    if boss_name == 'алдия, ученый первородного греха':
        return 0

    if 'заллен' in boss_name and 'луд' in boss_name:
        return only_digits(souls_items[0].split('/')[0])

    souls_value = souls_items[0]
    return only_digits(souls_value)


def parse(url: str, debug_log=False) -> List[Tuple[str, int, int]]:
    rows = []

    for category, bosses in get_bosses(url).items():
        debug_log and print(category)

        for boss in bosses:
            items = boss.get_boss_items()
            try:
                health = get_health(boss, items)
                souls = get_souls(boss, items)
                debug_log and print(f"    {boss.name}. Здоровье: {health}, души: {souls}")

                rows.append((boss.name, health, souls))

            except ValueError as e:
                debug_log and print(e)
                debug_log and print(boss.name)
                debug_log and print(items['Здоровье'])
                debug_log and print(items['Души'])
                debug_log and sys.exit()

        debug_log and print()

    return rows


def print_stats(
        rows: List[Tuple[str, int, int]],
        headers=('NAME', 'HEALTH', 'SOULS'),
        sort_column=1,
):
    rows.sort(key=lambda x: x[sort_column], reverse=True)

    rows.insert(0, headers)
    print_pretty_table(rows, align='<')
