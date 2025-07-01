#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import zoneinfo
from datetime import datetime, timedelta, timezone


tz_moscow = zoneinfo.ZoneInfo("Europe/Moscow")
tz_etc_0300 = zoneinfo.ZoneInfo("Etc/GMT-3")
tz_offset_0300 = timezone(offset=timedelta(minutes=3 * 60))
tz_offset_neg0300 = timezone(offset=timedelta(minutes=-3 * 60))
tz_utc = zoneinfo.ZoneInfo("UTC")

dt = datetime(year=2025, month=1, day=1, hour=12, minute=0, second=0)
print(dt)
# 2025-01-01 12:00:00

print()

dt_moscow = dt.replace(tzinfo=tz_moscow)
print(dt_moscow)
print(dt_moscow.astimezone(tz_utc).replace(tzinfo=None))
# 2025-01-01 12:00:00+03:00
# 2025-01-01 09:00:00

print()

dt_etc_0300 = dt.replace(tzinfo=tz_etc_0300)
print(dt_etc_0300)
print(dt_etc_0300.astimezone(tz_utc).replace(tzinfo=None))
# 2025-01-01 12:00:00+03:00
# 2025-01-01 09:00:00

print()

dt_offset_0300 = dt.replace(tzinfo=tz_offset_0300)
print(dt_offset_0300)
print(dt_offset_0300.astimezone(tz_utc).replace(tzinfo=None))
# 2025-01-01 12:00:00+03:00
# 2025-01-01 09:00:00

print()

dt_offset_neg0300 = dt.replace(tzinfo=tz_offset_neg0300)
print(dt_offset_neg0300)
print(dt_offset_neg0300.astimezone(tz_utc).replace(tzinfo=None))
# 2025-01-01 12:00:00-03:00
# 2025-01-01 15:00:00

print()

dt_utc = dt.replace(tzinfo=tz_utc)
print(dt_utc)
print(dt_utc.astimezone(tz_utc).replace(tzinfo=None))
# 2025-01-01 12:00:00+00:00
# 2025-01-01 12:00:00
