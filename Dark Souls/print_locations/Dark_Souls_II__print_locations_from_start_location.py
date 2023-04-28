#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
sys.path.append("..")

from common import get_links_location


# NOTE: Способ поиска локаций, начиная с начальной и через переходы локаций искать другие сработал, однако
# часть локаций потерялись -- не всегда на одной странице локации указывает переход на следующую, но это
# может быть в обратную сторону
# Поэтому, для большей надежности лучше использовать скрипт Dark_Souls_II__print_locations.py


def print_transitions(
    url: str,
    title: str,
    visited_locations: set,
    links: set,
    log: bool = True,
):
    title = title.strip().title()
    if title in visited_locations:
        return

    log and print(title, url)
    visited_locations.add(title)

    locations = get_links_location(url)
    if not locations:
        return locations

    if log:
        # Сначала напечатаем все связанные локации
        for x_title, x_url in locations:
            print(f"    {x_title} -> {x_url}")

        print()

    # Поищем у этих локаций связанные с ними локации
    for x_title, x_url in locations:
        # Проверяем что локации с обратной связью не занесены
        if (x_title, title) not in links:
            links.add((title, x_title))

        print_transitions(x_url, x_title, visited_locations, links, log)


if __name__ == "__main__":
    visited_locations = set()
    links = set()

    url_start_location = "http://ru.darksouls.wikia.com/wiki/Междумирье"
    print_transitions(url_start_location, "Междумирье", visited_locations, links)

    print()
    print(len(visited_locations), sorted(visited_locations))
    print(len(links), sorted(links))
