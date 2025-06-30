#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install pytz==2025.2
import pytz


ru_timezones: list[str] = pytz.country_timezones["ru"]
print(len(ru_timezones))
# 26

for tz in ru_timezones:
    print(tz)
"""
Europe/Kaliningrad
Europe/Moscow
Europe/Kirov
Europe/Volgograd
Europe/Astrakhan
Europe/Saratov
Europe/Ulyanovsk
Europe/Samara
Asia/Yekaterinburg
Asia/Omsk
Asia/Novosibirsk
Asia/Barnaul
Asia/Tomsk
Asia/Novokuznetsk
Asia/Krasnoyarsk
Asia/Irkutsk
Asia/Chita
Asia/Yakutsk
Asia/Khandyga
Asia/Vladivostok
Asia/Ust-Nera
Asia/Magadan
Asia/Sakhalin
Asia/Srednekolymsk
Asia/Kamchatka
Asia/Anadyr
"""
