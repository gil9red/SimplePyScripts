#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime, timedelta


def get_zero_time(dt: datetime) -> datetime:
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def get_items(
    start_dt: datetime,
    end_dt: datetime,
    delta: timedelta,
) -> list[tuple[datetime, datetime]]:
    items = []

    dt = end_dt
    while True:
        if dt <= start_dt:
            break

        dt1 = dt
        dt -= delta

        if dt < start_dt:
            dt = start_dt

        items.append((dt, dt1))

    return items


def to_ms(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)


dt = get_zero_time(datetime.utcnow())

for dt1, dt2 in get_items(
    start_dt=get_zero_time(dt - timedelta(weeks=6)),
    end_dt=get_zero_time(dt + timedelta(days=1)),
    delta=timedelta(weeks=1),
):
    print(f"{dt1} - {dt2}. {to_ms(dt1)}+{to_ms(dt2)}")
