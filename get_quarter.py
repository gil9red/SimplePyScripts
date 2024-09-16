#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import date, datetime


def get_quarter_num(month_or_date: date | datetime | int | None = None) -> int:
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


def get_quarter_roman(month_or_date: date | datetime | int | None = None) -> str:
    return ["I", "II", "III", "IV"][get_quarter_num(month_or_date) - 1]


if __name__ == "__main__":
    print(get_quarter_num())
    print(get_quarter_num(datetime.today()))
    print(get_quarter_num(date.today()))
    print()

    print(get_quarter_roman())
    print()

    for dt in [date(2018, month=i + 1, day=1) for i in range(12)]:
        print(dt, get_quarter_num(dt))

    assert get_quarter_num(1) == 1
    assert get_quarter_num(2) == 1
    assert get_quarter_num(3) == 1
    assert get_quarter_num(4) == 2
    assert get_quarter_num(5) == 2
    assert get_quarter_num(6) == 2
    assert get_quarter_num(7) == 3
    assert get_quarter_num(8) == 3
    assert get_quarter_num(9) == 3
    assert get_quarter_num(10) == 4
    assert get_quarter_num(11) == 4
    assert get_quarter_num(12) == 4

    assert get_quarter_roman(1) == "I"
    assert get_quarter_roman(2) == "I"
    assert get_quarter_roman(3) == "I"
    assert get_quarter_roman(4) == "II"
    assert get_quarter_roman(5) == "II"
    assert get_quarter_roman(6) == "II"
    assert get_quarter_roman(7) == "III"
    assert get_quarter_roman(8) == "III"
    assert get_quarter_roman(9) == "III"
    assert get_quarter_roman(10) == "IV"
    assert get_quarter_roman(11) == "IV"
    assert get_quarter_roman(12) == "IV"
