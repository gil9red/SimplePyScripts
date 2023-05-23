#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


def get_populations(url: str) -> dict:
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, "html.parser")

    # P1082 -- идентификатор для population
    population_node = root.select_one("#P1082")

    populations = dict()

    # Перебор строк в соседнем от population столбце
    for row in population_node.select(".wikibase-statementview"):
        # Небольшая хитрость -- берем только первые 2 значения, поидеи это будут: количество людей и дата
        number_str, data_str = row.select(".wikibase-snakview-value")[:2]

        # Вытаскиваем текст из
        number_str = number_str.text.strip()
        data_str = data_str.text.strip()

        # Делаем разделение и берем последнуюю часть, после приводим к числу
        # "1 July 2012" -> 2012, "2010" -> 2010
        year = int(data_str.split()[-1])

        # Добавляем в словарь
        populations[year] = number_str

    return populations


def get_population_by_year(populations: dict, year: int) -> str:
    # Если такой год не будет найден, вернем -1
    return populations.get(year, -1)


# Аналогично get_population_by_year, но сначала вытащит данные из
# указанного url, а после достанет значение по year
def get_population_from_url_by_year(url: str, year: int) -> str:
    populations = get_populations(url)
    return get_population_by_year(populations, year)


if __name__ == "__main__":
    url = "https://www.wikidata.org/wiki/Q148"
    populations = get_populations(url)
    print(populations)
    # {2012: '1,375,198,619', 2010: '1,359,755,102', 2015: '1,397,028,553', ...

    # Выводим данные с сортировкой по ключу: по возрастанию
    for year in sorted(populations):
        print("{}: {}".format(year, populations[year]))

    # 2010: 1,359,755,102
    # 2011: 1,367,480,264
    # 2012: 1,375,198,619
    # 2013: 1,382,793,212
    # 2014: 1,390,110,388
    # 2015: 1,397,028,553
    # 2016: 1,403,500,365
    # 2017: 1,409,517,397

    print(get_population_by_year(populations, 2012))  # 1,375,198,619
    print(get_population_by_year(populations, 2013))  # 1,382,793,212
    print(get_population_by_year(populations, 2014))  # 1,390,110,388
