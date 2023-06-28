#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import date, datetime


def get_quarter(month_or_date=None) -> int:
    dt = month_or_date
    if dt is None:
        dt = date.today()

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
        raise Exception(f'Invalid "month": {month}')


def get_quarter_num(month_or_date=None) -> str:
    return ["I", "II", "III", "IV"][get_quarter(month_or_date) - 1]


if __name__ == "__main__":
    print(get_quarter())
    print()
    print(get_quarter(datetime.today()))
    print(get_quarter(date.today()))
    print()
    print(get_quarter_num())
    print()

    for dt in [date(2018, month=i + 1, day=1) for i in range(12)]:
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

    assert get_quarter_num(1) == "I"
    assert get_quarter_num(2) == "I"
    assert get_quarter_num(3) == "I"
    assert get_quarter_num(4) == "II"
    assert get_quarter_num(5) == "II"
    assert get_quarter_num(6) == "II"
    assert get_quarter_num(7) == "III"
    assert get_quarter_num(8) == "III"
    assert get_quarter_num(9) == "III"
    assert get_quarter_num(10) == "IV"
    assert get_quarter_num(11) == "IV"
    assert get_quarter_num(12) == "IV"
