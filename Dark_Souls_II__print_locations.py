#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_transitions_location(url_location):
    """
    Функция для поиска переходов из локации

    """

    import requests
    rs = requests.get(url_location)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'lxml')

    transitions = list()

    table_transitions = root.select_one('table.pi-horizontal-group')
    if not table_transitions or 'Переходы:' not in table_transitions.text:
        return transitions

    for a in table_transitions.select('a'):
        from urllib.parse import urljoin
        url = urljoin(rs.url, a['href'])

        transitions.append((url, a.text))

    return transitions


if __name__ == '__main__':
    url = 'http://ru.darksouls.wikia.com/wiki/Категория:Локации_(Dark_Souls_II)?display=page&sort=alphabetical'

    import requests
    rs = requests.get(url)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'lxml')

    for a in root.select('#mw-pages .mw-content-ltr a'):
        rel_url = a['href']

        from urllib.parse import urljoin
        url = urljoin(rs.url, rel_url)

        transitions = get_transitions_location(url)
        if not transitions:
            continue

        print(a.text, url)
        for url_trans, title_trans in transitions:
            print('    {} -> {}'.format(title_trans, url_trans))

        print('\n')
