#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install pytz==2025.2
import pytz


timezones: list[str] = pytz.all_timezones
print(len(timezones), timezones)
# 594 ['Africa/Abidjan', 'Africa/Accra', 'Africa/Addis_Ababa', ..., 'W-SU', 'WET', 'Zulu']

timezones: list[str] = pytz.common_timezones
print(len(timezones), timezones)
# 439 ['Africa/Abidjan', 'Africa/Accra', 'Africa/Addis_Ababa', ..., 'US/Mountain', 'US/Pacific', 'UTC']
