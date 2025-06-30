#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime

# pip install pytz==2025.2
import pytz


tz_moscow = pytz.timezone("Europe/Moscow")
tz_etc_0300 = pytz.timezone("Etc/GMT-3")
tz_offset_0300 = pytz.FixedOffset(offset=3 * 60)
tz_utc = pytz.timezone("UTC")

dt = datetime(year=2025, month=1, day=1, hour=12, minute=0, second=0)
print(dt)
# 2025-01-01 12:00:00

print()

print(tz_moscow.fromutc(dt))
print(tz_etc_0300.fromutc(dt))
print(tz_offset_0300.fromutc(tz_offset_0300.localize(dt)))
print(tz_utc.fromutc(tz_utc.localize(dt)))
# 2025-01-01 15:00:00+03:00
# 2025-01-01 15:00:00+03:00
# 2025-01-01 15:00:00+03:00
# 2025-01-01 12:00:00+00:00
