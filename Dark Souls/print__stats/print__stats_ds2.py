#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from common import get_parsed_two_column_table_stats


def get_stats_ds2() -> [(str, str)]:
    url = 'http://ru.darksouls.wikia.com/wiki/Характеристики_(Dark_Souls_II)'
    return get_parsed_two_column_table_stats(url)


if __name__ == '__main__':
    items = get_stats_ds2()
    print(f'items ({len(items)}): {items}')
    print()

    # ['Адаптируемость', 'Вера', 'Жизненная сила', 'Интеллект', 'Ловкость', 'Сила', 'Стойкость', 'Уровень', 'Ученость', 'Физическая мощь']
    stats_titles = [x[0] for x in items]
    print(stats_titles)

    print()

    for title, description in items:
        print('{:20}: {}'.format(title, repr(description)))
