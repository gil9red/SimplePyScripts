#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime, date, timedelta


# Текущий день может отсутствовать, поэтому ищем ближайший день
# Например, если день 31, то ищем ближайший день 30
def correct_datetime(
    dt: datetime | date,
    target_year: int,
    target_month: int,
    target_day: int | None = None,
) -> datetime | date:
    # TODO: Можно ли упростить проверку, начиная ее для дня больше 28?
    #       target_day больше нужен для случаев, если день больше 28
    #       Можно явно перебирать дни вместе с месяцем и годом
    while True:
        try:
            dt = dt.replace(year=target_year, month=target_month)
            break
        except ValueError:
            dt -= timedelta(days=1)

    if target_day is not None:
        # Попробуем сразу указать target_day
        try:
            return dt.replace(day=target_day)
        except ValueError:
            pass

        # Стараемся найти день, ближайший к target_day
        start_day = min(dt.day, target_day)
        end_day = max(dt.day, target_day)

        for day in reversed(range(start_day, end_day + 1)):
            try:
                return dt.replace(day=day)
            except ValueError:
                pass

    return dt


if __name__ == "__main__":
    dt = datetime(year=2023, month=1, day=1, hour=12, minute=34, second=56)

    assert isinstance(
        correct_datetime(dt, target_year=2023, target_month=1),
        datetime,
    )
    assert isinstance(
        correct_datetime(dt.date(), target_year=2023, target_month=1),
        date,
    )

    assert correct_datetime(dt, dt.year, dt.month, dt.day) == dt
    assert correct_datetime(dt, dt.year, dt.month, dt.day + 1) == dt.replace(
        day=dt.day + 1
    )

    assert correct_datetime(dt.date(), dt.year, dt.month, dt.day) == dt.date()
    assert correct_datetime(
        dt.date(), dt.year, dt.month, dt.day + 1
    ) == dt.date().replace(day=dt.day + 1)

    assert correct_datetime(
        datetime(year=2023, month=1, day=1, hour=12, minute=34, second=56),
        target_year=2025,
        target_month=4,
    ) == datetime(year=2025, month=4, day=1, hour=12, minute=34, second=56)
    assert correct_datetime(
        datetime(year=2023, month=1, day=1, hour=12, minute=34, second=56),
        target_year=2025,
        target_month=4,
        target_day=30,
    ) == datetime(year=2025, month=4, day=30, hour=12, minute=34, second=56)
    assert correct_datetime(
        datetime(year=2023, month=1, day=1, hour=12, minute=34, second=56),
        target_year=2025,
        target_month=4,
        target_day=99,
    ) == datetime(year=2025, month=4, day=30, hour=12, minute=34, second=56)

    # Leap year
    assert correct_datetime(
        datetime(year=2024, month=2, day=29, hour=12, minute=34, second=56),
        target_year=2025,
        target_month=2,
    ) == datetime(year=2025, month=2, day=28, hour=12, minute=34, second=56)

    assert correct_datetime(
        datetime(year=2024, month=1, day=31, hour=12, minute=34, second=56),
        target_year=2024,
        target_month=2,
    ) == datetime(year=2024, month=2, day=29, hour=12, minute=34, second=56)
    assert correct_datetime(
        datetime(year=2024, month=1, day=31, hour=12, minute=34, second=56),
        target_year=2024,
        target_month=2,
        target_day=28,
    ) == datetime(year=2024, month=2, day=28, hour=12, minute=34, second=56)
    assert correct_datetime(
        datetime(year=2024, month=2, day=28, hour=12, minute=34, second=56),
        target_year=2024,
        target_month=1,
        target_day=31,
    ) == datetime(year=2024, month=1, day=31, hour=12, minute=34, second=56)
