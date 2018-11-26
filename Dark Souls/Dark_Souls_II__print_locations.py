#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from common import get_transitions_location


def find_locations() -> (set, set):
    URL = 'http://ru.darksouls.wikia.com/wiki/Категория:Локации_(Dark_Souls_II)?display=page&sort=alphabetical'

    visited_locations = set()
    global_transitions = set()

    rs = requests.get(URL)
    root = BeautifulSoup(rs.content, 'html.parser')

    for a in root.select('.category-page__member-link'):
        url = urljoin(rs.url, a['href'])

        transitions = get_transitions_location(url)
        if not transitions:
            continue

        title = a.text.strip().title()
        print(title, url)

        visited_locations.add(title)

        for url_trans, title_trans in transitions:
            title_trans = title_trans.title()
            print('    {} -> {}'.format(title_trans, url_trans))

            # Проверяем что локации с обратной связью не занесены
            if (title_trans, title) not in global_transitions:
                global_transitions.add((title, title_trans))

        print()

    return visited_locations, global_transitions


if __name__ == '__main__':
    visited_locations, global_transitions = find_locations()

    # Выведем итоговый список
    print(len(visited_locations), sorted(visited_locations))
    print(len(global_transitions), sorted(global_transitions))
