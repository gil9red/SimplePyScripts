#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_quarter(date__or__datetime=None) -> int:
    dt = date__or__datetime

    if dt is None:
        import datetime as DT
        dt = DT.date.today()

    month = dt.month

    if month in (1, 2, 3):
        return 1

    elif month in (4, 5, 6):
        return 2

    elif month in (7, 8, 9):
        return 3

    elif month in (10, 11, 12):
        return 4

    else:
        raise Exception('Invalid "month": {}'.format(month))


def get_current_quarter() -> int:
    return get_quarter()


if __name__ == '__main__':
    print(get_quarter())
    print(get_current_quarter())
    print()

    import datetime as DT

    print(get_quarter(DT.datetime.today()))
    print(get_quarter(DT.date.today()))
    print()

    for dt in [DT.date(2018, month=i + 1, day=1) for i in range(12)]:
        print(dt, get_quarter(dt))
