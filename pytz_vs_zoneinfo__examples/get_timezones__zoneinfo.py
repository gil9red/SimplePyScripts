#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import zoneinfo


timezones: list[str] = sorted(zoneinfo.available_timezones())
print(len(timezones), timezones)
# 597 ['Africa/Abidjan', 'Africa/Accra', 'Africa/Addis_Ababa', ..., 'W-SU', 'WET', 'Zulu']
