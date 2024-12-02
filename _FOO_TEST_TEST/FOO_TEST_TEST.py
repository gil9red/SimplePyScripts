#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime, timedelta


def get_zero_time(dt: datetime) -> datetime:
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def to_ms(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)


dt = get_zero_time(datetime.utcnow())
dt1 = get_zero_time(dt - timedelta(days=1))
dt2 = get_zero_time(dt + timedelta(days=1))

print(to_ms(dt1), dt1)
print(to_ms(dt2), dt2)
print(f"{to_ms(dt1)}+{to_ms(dt2)}")
