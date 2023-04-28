#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from bs4 import BeautifulSoup
import requests


def get_class_by_stats() -> dict[str, dict[str, int]]:
    url = "https://demonssouls.fandom.com/ru/wiki/Классы"

    rs = requests.get(url)
    root = BeautifulSoup(rs.content, "html.parser")

    class_by_stats = dict()

    for tr in root.select("table > tr"):
        td_list = [td.get_text(strip=True) for td in tr.select("td")]
        if not td_list:
            continue

        class_name = td_list[0]
        stats = list(map(int, td_list[1:]))

        class_by_stats[class_name] = {
            "Жизненная сила": stats[0],
            "Интеллект": stats[1],
            "Стойкость": stats[2],
            "Сила": stats[3],
            "Ловкость": stats[4],
            "Магия": stats[5],
            "Вера": stats[6],
            "Удача": stats[7],
            "Уровень души": stats[8],
        }

    return class_by_stats


if __name__ == "__main__":
    class_by_stats = get_class_by_stats()
    print(class_by_stats)

    print()

    for class_name, stats in sorted(
        class_by_stats.items(), key=lambda x: x[1]["Уровень души"]
    ):
        total_stats = sum(list(stats.values())[:-1])
        print(
            f'{class_name} (level={stats["Уровень души"]}), total stats: {total_stats}'
        )
    # Дворянин (level=1), total stats: 81
    # Рыцарь (level=4), total stats: 84
    # Храмовник (level=4), total stats: 84
    # Солдат (level=6), total stats: 86
    # Охотник (level=6), total stats: 86
    # Жрец (level=6), total stats: 86
    # Маг (level=6), total stats: 86
    # Странник (level=6), total stats: 86
    # Варвар (level=9), total stats: 89
    # Вор (level=9), total stats: 89

    print()

    for class_name, stats in class_by_stats.items():
        print(f"{class_name}: {stats}")
    """
    Солдат: {'Жизненная сила': 14, 'Интеллект': 9, 'Стойкость': 12, 'Сила': 12, 'Ловкость': 11, 'Магия': 8, 'Вера': 10, 'Удача': 10, 'Уровень души': 6}
    Рыцарь: {'Жизненная сила': 10, 'Интеллект': 11, 'Стойкость': 11, 'Сила': 14, 'Ловкость': 10, 'Магия': 10, 'Вера': 11, 'Удача': 7, 'Уровень души': 4}
    Охотник: {'Жизненная сила': 12, 'Интеллект': 10, 'Стойкость': 13, 'Сила': 11, 'Ловкость': 12, 'Магия': 8, 'Вера': 8, 'Удача': 12, 'Уровень души': 6}
    Жрец: {'Жизненная сила': 13, 'Интеллект': 11, 'Стойкость': 12, 'Сила': 13, 'Ловкость': 8, 'Магия': 8, 'Вера': 13, 'Удача': 8, 'Уровень души': 6}
    Маг: {'Жизненная сила': 9, 'Интеллект': 15, 'Стойкость': 10, 'Сила': 9, 'Ловкость': 11, 'Магия': 15, 'Вера': 6, 'Удача': 11, 'Уровень души': 6}
    Странник: {'Жизненная сила': 10, 'Интеллект': 10, 'Стойкость': 11, 'Сила': 11, 'Ловкость': 15, 'Магия': 9, 'Вера': 7, 'Удача': 13, 'Уровень души': 6}
    Варвар: {'Жизненная сила': 15, 'Интеллект': 7, 'Стойкость': 13, 'Сила': 15, 'Ловкость': 9, 'Магия': 11, 'Вера': 8, 'Удача': 11, 'Уровень души': 9}
    Вор: {'Жизненная сила': 10, 'Интеллект': 13, 'Стойкость': 10, 'Сила': 9, 'Ловкость': 14, 'Магия': 10, 'Вера': 8, 'Удача': 15, 'Уровень души': 9}
    Храмовник: {'Жизненная сила': 11, 'Интеллект': 8, 'Стойкость': 13, 'Сила': 14, 'Ловкость': 12, 'Магия': 6, 'Вера': 13, 'Удача': 7, 'Уровень души': 4}
    Дворянин: {'Жизненная сила': 8, 'Интеллект': 12, 'Стойкость': 8, 'Сила': 9, 'Ловкость': 12, 'Магия': 13, 'Вера': 12, 'Удача': 7, 'Уровень души': 1}
    """
