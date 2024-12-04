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
print(dt)
# 2024-12-04 00:00:00

for dt1, dt2 in get_items(
    start_dt=get_zero_time(dt - timedelta(weeks=6)),
    end_dt=get_zero_time(dt + timedelta(days=1)),
    delta=timedelta(weeks=1),
):
    print(f"{dt1} - {dt2}. {to_ms(dt1)}+{to_ms(dt2)}")
"""
2024-11-28 00:00:00 - 2024-12-05 00:00:00. 1732734000000+1733338800000
2024-11-21 00:00:00 - 2024-11-28 00:00:00. 1732129200000+1732734000000
2024-11-14 00:00:00 - 2024-11-21 00:00:00. 1731524400000+1732129200000
2024-11-07 00:00:00 - 2024-11-14 00:00:00. 1730919600000+1731524400000
2024-10-31 00:00:00 - 2024-11-07 00:00:00. 1730314800000+1730919600000
2024-10-24 00:00:00 - 2024-10-31 00:00:00. 1729710000000+1730314800000
2024-10-23 00:00:00 - 2024-10-24 00:00:00. 1729623600000+1729710000000
"""
