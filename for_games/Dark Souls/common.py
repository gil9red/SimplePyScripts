#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from collections import defaultdict
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


URL_DS1 = "http://ru.darksouls.wikia.com/wiki/Категория:Локации_(Dark_Souls)"
URL_DS2 = "http://ru.darksouls.wikia.com/wiki/Категория:Локации_(Dark_Souls_II)"
URL_DS3 = "http://ru.darksouls.wikia.com/wiki/Категория:Локации_(Dark_Souls_III)"


class Parser:
    def __init__(self, url_locations: str, log=True):
        self._url_locations = url_locations
        self._is_log = log

        self._visited_locations: list[str] = []
        self._links: list[tuple[str, str]] = []
        self._link_boss: list[tuple[str, str]] = []

        self._location_by_url: dict[str, str] = dict()
        self._boss_by_url: dict[str, str] = dict()

        self._bosses: list[str] = []
        self._location_by_bosses: dict[str, list[tuple[str, str]]] = defaultdict(list)

    @staticmethod
    def DS1(log=True) -> "Parser":
        return Parser(URL_DS1, log)

    @staticmethod
    def DS2(log=True) -> "Parser":
        return Parser(URL_DS2, log)

    @staticmethod
    def DS3(log=True) -> "Parser":
        return Parser(URL_DS3, log)

    def _log(self, *args, **kwargs):
        self._is_log and print(*args, **kwargs)

    @staticmethod
    def __fix_title(title: str) -> str:
        # Для удобства обработки приводим к одному регистру
        title = title.lower().strip()

        # Удаляем из названий " (Dark Souls III)"
        title = title.replace("(dark souls iii)", "").strip()

        # Исправляем название "Крепость Сен" -> "Крепость Сена"
        if title == "крепость сен":
            title = "крепость сена"

        # В переходах "Темная Бездна Былого" было указано "Темные руины", но имеется ввиду локация "Темнолесье"
        if title == "темные руины":
            title = "темнолесье"

        # Приводим к общему виду
        return title.title()

    @staticmethod
    def get_links_location(url_location: str) -> list[tuple[str, str]]:
        """
        Функция для поиска переходов из локации

        """

        rs = requests.get(url_location)
        root = BeautifulSoup(rs.content, "html.parser")

        table_locations = None

        for table in root.select("table.pi-horizontal-group"):
            if "Переходы:" in table.text:
                table_locations = table
                break

        locations = []

        # Если не нашли
        if not table_locations:
            return locations

        for a in table_locations.select("a"):
            url = urljoin(rs.url, a["href"])
            title = Parser.__fix_title(a.text)

            locations.append((title, url))

        return locations

    @staticmethod
    def get_bosses_by_location(url_location: str) -> list[tuple[str, str]]:
        """
        Функция для поиска боссов локации

        """

        rs = requests.get(url_location)
        root = BeautifulSoup(rs.content, "html.parser")

        table_bosses = None

        for table in root.select("table.pi-horizontal-group"):
            if "Босс локации:" in table.text:
                table_bosses = table
                break

        bosses = []

        # Если не нашли
        if not table_bosses:
            return bosses

        for a in table_bosses.select("a"):
            url = urljoin(rs.url, a["href"])
            title = Parser.__fix_title(a.text)

            bosses.append((title, url))

        return bosses

    def parse(self) -> "Parser":
        visited_locations = set()
        links = set()
        link_boss = set()

        rs = requests.get(self._url_locations)
        root = BeautifulSoup(rs.content, "html.parser")

        for a in root.select(".category-page__member-link"):
            abs_url = urljoin(rs.url, a["href"])

            # У любой локации есть связанная с ней локация. Если нет -- значит это страница
            # не про локацию
            locations = self.get_links_location(abs_url)
            if not locations:
                continue

            title = Parser.__fix_title(a.text)
            visited_locations.add(title)

            self._location_by_url[title] = abs_url

            self._log(title, abs_url)
            self._log("    Переходы:")

            # Найдем связанные локации
            for x_title, x_url in locations:
                self._log(f"        {x_title} -> {x_url}")
                self._location_by_url[x_title] = x_url

                # Проверяем что локации с обратной связью не занесены
                if (x_title, title) not in links:
                    links.add((title, x_title))

            self._log("    Боссы:")

            # Найдем боссов локации
            bosses = self.get_bosses_by_location(abs_url)
            self._location_by_bosses[title] += bosses

            for boss_name, boss_url in bosses:
                self._log(f"        {boss_name} -> {boss_url}")
                self._boss_by_url[boss_name] = boss_url
                self._bosses.append(boss_name)

                link_boss.add((title, boss_name))

            self._log()

        self._visited_locations = sorted(visited_locations)
        self._links = sorted(links)
        self._link_boss = sorted(link_boss)

        return self

    def get_url_locations(self) -> str:
        return self._url_locations

    def get_locations(self) -> list[str]:
        return self._visited_locations

    def get_links(self) -> list[tuple[str, str]]:
        return self._links

    def get_bosses(self) -> list[str]:
        return self._bosses

    def get_bosses_of_location(self) -> list[tuple[str, str]]:
        return self._link_boss

    def get_location_by_bosses(
        self, location_name: str = None
    ) -> dict[str, list[tuple[str, str]]] | list[tuple[str, str]]:
        if location_name is None:
            return self._location_by_bosses

        return self._location_by_bosses.get(location_name)

    def get_location_by_url(
        self, location_name: str = None
    ) -> dict[str, str] | str:
        if location_name is None:
            return self._location_by_url

        return self._location_by_url.get(location_name)

    def get_boss_by_url(self, boss_name: str = None) -> dict[str, str] | str:
        if boss_name is None:
            return self._boss_by_url

        return self._boss_by_url.get(boss_name)


def get_links_location(url_location: str) -> list[tuple[str, str]]:
    """
    Функция для поиска переходов из локации

    """

    return Parser.get_links_location(url_location)


def get_bosses_by_location(url_location: str) -> list[tuple[str, str]]:
    """
    Функция для поиска боссов локации

    """

    return Parser.get_bosses_by_location(url_location)


def parse_locations(
    url_locations: str, log=True
) -> tuple[list[str], list[tuple[str, str]], list[tuple[str, str]]]:
    p = Parser(url_locations, log).parse()
    return p.get_locations(), p.get_links(), p.get_bosses_of_location()


def parse_locations_ds1(
    log=True,
) -> tuple[list[str], list[tuple[str, str]], list[tuple[str, str]]]:
    return parse_locations(URL_DS1, log)


def parse_locations_ds2(
    log=True,
) -> tuple[list[str], list[tuple[str, str]], list[tuple[str, str]]]:
    return parse_locations(URL_DS2, log)


def parse_locations_ds3(
    log=True,
) -> tuple[list[str], list[tuple[str, str]], list[tuple[str, str]]]:
    return parse_locations(URL_DS3, log)


def find_links_ds1(log=True) -> list[tuple[str, str]]:
    return parse_locations_ds1(log)[1]


def find_links_ds2(log=True) -> list[tuple[str, str]]:
    return parse_locations_ds2(log)[1]


def find_links_ds3(log=True) -> list[tuple[str, str]]:
    return parse_locations_ds3(log)[1]


def find_bosses_of_location_ds1(log=True) -> list[tuple[str, str]]:
    return parse_locations_ds1(log)[2]


def find_bosses_of_location_ds2(log=True) -> list[tuple[str, str]]:
    return parse_locations_ds2(log)[2]


def find_bosses_of_location_ds3(log=True) -> list[tuple[str, str]]:
    return parse_locations_ds3(log)[2]


if __name__ == "__main__":
    visited_locations, links, link_boss = parse_locations_ds1()

    # Выведем итоговый список
    print(len(visited_locations), visited_locations)
    print(len(links), links)
    print(len(link_boss), link_boss)

    print()

    links = find_links_ds1(log=False)
    print(len(links), links)

    print()

    # DS1
    bosses = get_bosses_by_location(
        "http://ru.darksouls.wikia.com/wiki/Северное_Прибежище_Нежити"
    )
    print(len(bosses), bosses)

    # DS2
    bosses = get_bosses_by_location("http://ru.darksouls.wikia.com/wiki/Маджула")
    print(len(bosses), bosses)

    # DS3
    bosses = get_bosses_by_location(
        "http://ru.darksouls.wikia.com/wiki/Анор_Лондо_(Dark_Souls_III)"
    )
    print(len(bosses), bosses)

    print()

    p = Parser(URL_DS1, log=False).parse()
    # OR:
    # p = ParserDS1(log=False).parse()
    print("get_url_locations:", p.get_url_locations())
    print("get_locations:", p.get_locations())
    print("get_bosses:", p.get_bosses())
    print("get_links:", p.get_links())
    print("get_bosses_of_location:", p.get_bosses_of_location())
    print("get_boss_by_url:", p.get_boss_by_url())
    print("get_location_by_url:", p.get_location_by_url())
