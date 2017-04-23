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
    visited_locations = set()

    def print_transitions(url, title):
        title = title.lower().strip()

        if title in visited_locations:
            return

        visited_locations.add(title)
        print(title.title(), url)

        transitions = get_transitions_location(url)
        if not transitions:
            return transitions

        # Сначала напечатаем все связанные локации
        for url_trans, title_trans in transitions:
            print('    {} -> {}'.format(title_trans.title().strip(), url_trans))

        print('\n')

        # Поищем у этих локаций связаные с ними локации
        for url_trans, title_trans in transitions:
            title_trans = title_trans.lower().strip()

            if title_trans not in visited_locations:
                print_transitions(url_trans, title_trans)


    url_start_location = 'http://ru.darksouls.wikia.com/wiki/%D0%9C%D0%B5%D0%B6%D0%B4%D1%83%D0%BC%D0%B8%D1%80%D1%8C%D0%B5'
    print_transitions(url_start_location, 'Междумирье')

    print()
    print(len(visited_locations), [_.title() for _ in visited_locations])
