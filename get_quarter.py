#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT


def get_quarter(month_or_date=None) -> int:
    dt = month_or_date
    if dt is None:
        dt = DT.date.today()

    if isinstance(dt, int):
        month = dt
    else:
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


if __name__ == '__main__':
    print(get_quarter())
    print()
    print(get_quarter(DT.datetime.today()))
    print(get_quarter(DT.date.today()))
    print()

    for dt in [DT.date(2018, month=i + 1, day=1) for i in range(12)]:
        print(dt, get_quarter(dt))

    assert get_quarter(1) == 1
    assert get_quarter(2) == 1
    assert get_quarter(3) == 1
    assert get_quarter(4) == 2
    assert get_quarter(5) == 2
    assert get_quarter(6) == 2
    assert get_quarter(7) == 3
    assert get_quarter(8) == 3
    assert get_quarter(9) == 3
    assert get_quarter(10) == 4
    assert get_quarter(11) == 4
    assert get_quarter(12) == 4
