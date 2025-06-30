#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install pytz==2025.2
import pytz


tz_moscow = pytz.timezone("Europe/Moscow")
print(tz_moscow)
# Europe/Moscow

tz_utc = pytz.timezone("UTC")
print(tz_utc)
# UTC

try:
    tz = pytz.timezone("INVALID")
    raise Exception()
except pytz.UnknownTimeZoneError as e:
    print(e)
# 'INVALID'

try:
    tz = pytz.timezone(None)
    raise Exception()
except pytz.UnknownTimeZoneError as e:
    print(e)
# None
