#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_bosses(url: str) -> dict([]):
    from urllib.parse import urljoin

    import requests
    rs = requests.get(url)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'html.parser')

    from collections import defaultdict
    bosses_by_category = defaultdict(list)

    category_name = None

    for tr in root.select('table tr'):
        # Заголовок первым идет
        th = tr.select_one('th')
        if th:
            category_name = th.text.strip().upper()
            continue

        if not category_name:
            continue

        td_list = [(td.text.strip(), urljoin(rs.url, td.select_one('a')['href']))
                   for td in tr.select('td') if td.text.strip()]

        bosses_by_category[category_name] += td_list

    return bosses_by_category


def print_bosses(url, bosses: dict([])):
    print('{} ({})):'.format(url, sum([len(i) for i in bosses.values()])))

    for category, bosses in bosses.items():
        print('{} ({}):'.format(category, len(bosses)))

        for i, (boss_name, boss_url) in enumerate(bosses, 1):
            print('    {}. "{}": {}'.format(i, boss_name, boss_url))

        print()

    print()


def export_to_json(file_name, bosses):
    import json
    json.dump(bosses, open(file_name, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)


if __name__ == '__main__':
    url = 'http://ru.darksouls.wikia.com/wiki/Боссы'
    bosses_ds1 = get_bosses(url)
    print_bosses(url, bosses_ds1)
    export_to_json('bosses_ds1.json', bosses_ds1)

    url = 'http://ru.darksouls.wikia.com/wiki/Боссы_(Dark_Souls_II)'
    bosses_ds2 = get_bosses(url)
    print_bosses(url, bosses_ds2)
    export_to_json('bosses_ds2.json', bosses_ds2)

    url = 'http://ru.darksouls.wikia.com/wiki/Боссы_(Dark_Souls_III)'
    bosses_ds3 = get_bosses(url)
    print_bosses(url, bosses_ds3)
    export_to_json('bosses_ds3.json', bosses_ds3)
