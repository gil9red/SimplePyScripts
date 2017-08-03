#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для анализа популярности имен и выдачи топа из 10 имен.
Пример:

    Total: 384
    Top 10:
        Дмитрий: 20
        Александр: 18
        Елена: 15
        Евгений: 15
        Сергей: 14
        Алексей: 12
        Ольга: 11
        Илья: 10
        Денис: 10
        Владимир: 9

"""


if __name__ == '__main__':
    from get_user_and_deviation_hours import get_report_context
    text = get_report_context()

    from bs4 import BeautifulSoup
    root = BeautifulSoup(text, 'lxml')

    # Имена описаны как "<Фамилия> <Имя> <Отчество>"
    first_name_list = [report.text.split()[1].strip() for report in root.select('#report .person')]

    print('Total:', len(first_name_list))

    print('Top 10:')
    from collections import Counter
    counter = Counter(first_name_list)

    # Сортировка по количеству
    for name, number in sorted(counter.items(), key=lambda x: x[1], reverse=True)[:10]:
        print('    {}: {}'.format(name, number))
