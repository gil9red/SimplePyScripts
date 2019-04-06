#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# source: http://stackoverflow.com/a/5910078/5909792
def ascii_table(rows, headers):
    lens = list()
    for i in range(len(headers)):
        lens.append(
            len(
                max(
                    [str(x[i]) for x in rows] + [headers[i]],
                    key=lambda x: len(str(x))
                )
            )
        )

    formats = ["%%-%ds" % col_len for col_len in lens]

    pattern = " | ".join(formats)
    hpattern = " | ".join(formats)
    separator = "-+-".join(['-' * n for n in lens])

    text_lines = [hpattern % tuple(headers), separator]
    for line in rows:
        text_lines.append(pattern % tuple(t for t in line))

    return '\n'.join(text_lines)


def print_the_most_profitable_dish(url):
    print(url)

    import requests
    rs = requests.get(url)
    print(rs)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'lxml')

    unknown_metrics_items = []
    items = []

    import re

    for i, product in enumerate(root.select('.CardContent'), 1):
        title = product.select_one('.CardText__title').text.strip()

        price = product.select_one('.ProductParams__price').text
        price = int(re.sub('\D', '', price))

        try:
            tag_subtitle = product.select_one('.CardText__subtitle > span > b').text.strip()
            weight, metrics = tag_subtitle.split()

        except Exception:
            unknown_metrics_items.append((title, price))
            continue

        # Ignore
        if metrics not in ['кг.', 'гр.']:
            unknown_metrics_items.append((title, tag_subtitle, price))
            continue

        weight = float(weight)
        if metrics == 'кг.':
            weight *= 1000

        # print('{}. "{}": {} гр., {} -> {:.3f}'.format(i, title, weight, price, weight / price))
        items.append((title, weight, price, weight / price))

    print('Самые выгодные по количеству грамм за единицу цены:')
    print()

    items.sort(key=lambda x: x[3], reverse=True)
    items = [(title, weight, price, '{:.3f}'.format(rate)) for title, weight, price, rate in items]

    columns = ['Название', 'Вес (гр.)', 'Цена', 'Коэффициент']
    print(ascii_table(items, columns))
    #
    # OR:
    # for i, (title, weight, price, rate) in enumerate(sorted(items, key=lambda x: x[3], reverse=True), 1):
    #     print('  {}. "{}": {} гр., {} -> {:.3f}'.format(i, title, weight, price, rate))

    if unknown_metrics_items:
        print()
        print('Неудалось обработать:')
        for i, item in enumerate(unknown_metrics_items, 1):
            print('  {}. {}'.format(i, ', '.join(map(str, item))))


if __name__ == '__main__':
    urls = [
        'http://sushivkusno.com/category/nabory-siety',
        'http://sushivkusno.com/category/goriachiie-zakuski',
        'http://sushivkusno.com/category/salaty',
    ]

    for url in urls:
        print_the_most_profitable_dish(url)
        print('\n')
