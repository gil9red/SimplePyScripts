#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime

# pip install pytz==2025.2
import pytz


tz_moscow = pytz.timezone("Europe/Moscow")
print(tz_moscow)
# Europe/Moscow

tz_etc_0300 = pytz.timezone("Etc/GMT-3")
print(tz_etc_0300)
# Etc/GMT-3

tz_offset_0300 = pytz.FixedOffset(offset=3 * 60)
print(tz_offset_0300)
# pytz.FixedOffset(180)

tz_utc = pytz.timezone("UTC")
print(tz_utc)
# UTC

print()

dt = datetime(year=2025, month=1, day=1, hour=12, minute=0, second=0)

print(dt.astimezone(tz_moscow).strftime("%z"))
print(dt.astimezone(tz_etc_0300).strftime("%z"))
print(dt.astimezone(tz_offset_0300).strftime("%z"))
print(dt.astimezone(tz_utc).strftime("%z"))
# +0300
# +0300
# +0300
# +0000
