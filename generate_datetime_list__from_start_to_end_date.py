#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT


def generate_datetime_list(start_date, end_date) -> list:
    date_1 = min(start_date, end_date)
    date_2 = max(start_date, end_date)

    # Сразу добавляем стартовую дату
    items = [date_1]

    i = 1

    while date_1 < date_2:
        date_1 += DT.timedelta(days=i)
        items.append(date_1)

    return items


if __name__ == '__main__':
    def d2s(date):
        return date.strftime("%d/%m/%Y")

    start_date = DT.datetime(2018, 8, 13)
    end_date = DT.datetime(2018, 8, 1)
    print(d2s(start_date), d2s(end_date))

    items = generate_datetime_list(start_date, end_date)
    print('Items ({}): {}'.format(len(items), items))

    for date in items:
        print(d2s(date))
