#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import zoneinfo
from datetime import datetime, timedelta, timezone


tz_moscow = zoneinfo.ZoneInfo("Europe/Moscow")
tz_etc_0300 = zoneinfo.ZoneInfo("Etc/GMT-3")
tz_offset_0300 = timezone(offset=timedelta(minutes=3 * 60))
tz_utc = zoneinfo.ZoneInfo("UTC")

dt_utc = datetime(year=2025, month=1, day=1, hour=12, minute=0, second=0, tzinfo=tz_utc)
print(dt_utc)
# 2025-01-01 12:00:00+00:00

assert dt_utc == datetime.fromisoformat("2025-01-01 12:00:00").replace(tzinfo=dt_utc.tzinfo)
assert dt_utc == datetime.fromisoformat("2025-01-01 12:00:00").replace(tzinfo=timezone.utc)

print()

print(dt_utc.astimezone(tz_moscow))
print(dt_utc.astimezone(tz_etc_0300))
print(dt_utc.astimezone(tz_offset_0300))
print(dt_utc.astimezone(tz_utc))
# 2025-01-01 15:00:00+03:00
# 2025-01-01 15:00:00+03:00
# 2025-01-01 15:00:00+03:00
# 2025-01-01 12:00:00+00:00

print("\n" + "-" * 10 + "\n")

dt = datetime(year=2025, month=1, day=1, hour=12, minute=0, second=0)
print(dt)
# 2025-01-01 12:00:00

print()

print(tz_moscow.fromutc(dt.replace(tzinfo=tz_moscow)))
print(tz_etc_0300.fromutc(dt.replace(tzinfo=tz_etc_0300)))
print(tz_offset_0300.fromutc(dt.replace(tzinfo=tz_offset_0300)))
print(tz_utc.fromutc(dt.replace(tzinfo=tz_utc)))
# 2025-01-01 15:00:00+03:00
# 2025-01-01 15:00:00+03:00
# 2025-01-01 15:00:00+03:00
# 2025-01-01 12:00:00+00:00
