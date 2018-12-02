#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List, Tuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def __fix_title(title: str) -> str:
    # Для удобства обработки приводим к одному регистру
    title = title.lower().strip()

    # Удаляем из названий " (Dark Souls III)"
    title = title.replace('(dark souls iii)', '').strip()

    # Исправляем название "Крепость Сен" -> "Крепость Сена"
    if title == 'крепость сен':
        title = 'крепость сена'

    # Приводим к общему виду
    return title.title()


def get_links_location(url_location: str) -> List[Tuple[str, str]]:
    """
    Функция для поиска переходов из локации

    """

    rs = requests.get(url_location)
    root = BeautifulSoup(rs.content, 'html.parser')

    table_locations = None

    for table in root.select('table.pi-horizontal-group'):
        if 'Переходы:' in table.text:
            table_locations = table
            break

    locations = []

    # Если не нашли
    if not table_locations:
        return locations

    for a in table_locations.select('a'):
        url = urljoin(rs.url, a['href'])
        title = __fix_title(a.text)

        locations.append((title, url))

    return locations


def get_bosses_of_location(url_location: str) -> List[Tuple[str, str]]:
    """
    Функция для поиска боссов локации

    """

    rs = requests.get(url_location)
    root = BeautifulSoup(rs.content, 'html.parser')

    table_bosses = None

    for table in root.select('table.pi-horizontal-group'):
        if 'Босс локации:' in table.text:
            table_bosses = table
            break

    bosses = []

    # Если не нашли
    if not table_bosses:
        return bosses

    for a in table_bosses.select('a'):
        url = urljoin(rs.url, a['href'])
        title = __fix_title(a.text)

        bosses.append((title, url))

    return bosses


def parse_locations(url_locations: str, log=True) -> (List[str], List[Tuple[str, str]], List[Tuple[str, str]]):
    visited_locations = set()
    links = set()
    link_boss = set()

    rs = requests.get(url_locations)
    root = BeautifulSoup(rs.content, 'html.parser')

    for a in root.select('.category-page__member-link'):
        abs_url = urljoin(rs.url, a['href'])

        # У любой локации есть связанная с ней локация. Если нет -- значит это страница
        # не про локацию
        locations = get_links_location(abs_url)
        if not locations:
            continue

        title = __fix_title(a.text)
        visited_locations.add(title)

        log and print(title, abs_url)
        log and print('    Переходы:')

        # Найдем связанные локации
        for x_title, x_url in locations:
            log and print('        {} -> {}'.format(x_title, x_url))

            # Проверяем что локации с обратной связью не занесены
            if (x_title, title) not in links:
                links.add((title, x_title))

        log and print('    Боссы:')

        # Найдем боссов локации
        for boss_name, boss_url in get_bosses_of_location(abs_url):
            log and print('        {} -> {}'.format(boss_name, boss_url))

            link_boss.add((title, boss_name))

        log and print()

    visited_locations = sorted(visited_locations)
    links = sorted(links)
    link_boss = sorted(link_boss)

    return visited_locations, links, link_boss


def parse_locations_ds1(log=True) -> (List[str], List[Tuple[str, str]], List[Tuple[str, str]]):
    url = "http://ru.darksouls.wikia.com/wiki/Категория:Локации_(Dark_Souls)"
    return parse_locations(url, log)


def parse_locations_ds2(log=True) -> (List[str], List[Tuple[str, str]], List[Tuple[str, str]]):
    url = "http://ru.darksouls.wikia.com/wiki/Категория:Локации_(Dark_Souls_II)"
    return parse_locations(url, log)


def parse_locations_ds3(log=True) -> (List[str], List[Tuple[str, str]], List[Tuple[str, str]]):
    url = "http://ru.darksouls.wikia.com/wiki/Категория:Локации_(Dark_Souls_III)"
    return parse_locations(url, log)


def find_links_ds1(log=True) -> List[Tuple[str, str]]:
    return parse_locations_ds1(log)[1]


def find_links_ds2(log=True) -> List[Tuple[str, str]]:
    return parse_locations_ds2(log)[1]


def find_links_ds3(log=True) -> List[Tuple[str, str]]:
    return parse_locations_ds3(log)[1]


def find_bosses_of_location_ds1(log=True) -> List[Tuple[str, str]]:
    return parse_locations_ds1(log)[2]


def find_bosses_of_location_ds2(log=True) -> List[Tuple[str, str]]:
    return parse_locations_ds2(log)[2]


def find_bosses_of_location_ds3(log=True) -> List[Tuple[str, str]]:
    return parse_locations_ds3(log)[2]


if __name__ == '__main__':
    visited_locations, links, bosses = parse_locations_ds1()

    # Выведем итоговый список
    print(len(visited_locations), visited_locations)
    print(len(links), links)
    print(len(bosses), bosses)

    print()

    links = find_links_ds1(log=False)
    print(len(links), links)

    print()

    # DS1
    bosses = get_bosses_of_location('http://ru.darksouls.wikia.com/wiki/Северное_Прибежище_Нежити')
    print(len(bosses), bosses)

    # DS2
    bosses = get_bosses_of_location('http://ru.darksouls.wikia.com/wiki/Маджула')
    print(len(bosses), bosses)

    # DS3
    bosses = get_bosses_of_location('http://ru.darksouls.wikia.com/wiki/Анор_Лондо_(Dark_Souls_III)')
    print(len(bosses), bosses)
