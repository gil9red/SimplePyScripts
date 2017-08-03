#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для анализа популярности имен и выдачи топа из 10 имен.

Пример:
    Total: 384
    Top 10:
        Дмитрий: 20 (5.2%)
        Александр: 18 (4.7%)
        Евгений: 15 (3.9%)
        Елена: 15 (3.9%)
        Сергей: 14 (3.6%)
        Алексей: 12 (3.1%)
        Ольга: 11 (2.9%)
        Денис: 10 (2.6%)
        Илья: 10 (2.6%)
        Владимир: 9 (2.3%)

"""


if __name__ == '__main__':
    from get_user_and_deviation_hours import get_report_context
    text = get_report_context()

    from bs4 import BeautifulSoup
    root = BeautifulSoup(text, 'lxml')

    # Имена описаны как "<Фамилия> <Имя> <Отчество>"
    first_name_list = [report.text.split()[1].strip() for report in root.select('#report .person')]

    total = len(first_name_list)
    print('Total:', total)

    print('Top 10:')
    from collections import Counter
    counter = Counter(first_name_list)

    # Сортировка по количеству
    for name, number in sorted(counter.items(), key=lambda x: x[1], reverse=True)[:10]:
        print('    {}: {} ({:.1f}%)'.format(name, number, number * 100 / total))
