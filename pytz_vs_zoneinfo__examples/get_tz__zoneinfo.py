#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import zoneinfo
from datetime import datetime, timedelta, timezone


tz_moscow = zoneinfo.ZoneInfo("Europe/Moscow")
print(tz_moscow)
# Europe/Moscow

tz_utc = zoneinfo.ZoneInfo("UTC")
print(tz_utc)
# UTC

try:
    tz = zoneinfo.ZoneInfo("INVALID")
    raise Exception()
except zoneinfo.ZoneInfoNotFoundError as e:
    print(e)
# 'No time zone found with key INVALID'
