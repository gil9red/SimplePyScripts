#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: append humanize example: https://github.com/jmoiron/humanize


# pip install humanize
import humanize


# Integer humanization:
print(humanize.intcomma(12345))      # '12,345'
print(humanize.intcomma(123456789))  # '123,456,789'
print()

print(humanize.intword(123455913))      # '123.5 million'
print(humanize.intword(12345591313))    # '12.3 billion'
print(humanize.intword(1339014900000))  # '1.3 trillion'
print()

print(humanize.apnumber(4))   # 'four'
print(humanize.apnumber(7))   # 'seven'
print(humanize.apnumber(41))  # '41'
print()


# Date & time humanization:
import datetime as DT
print(humanize.naturalday(DT.datetime.now()))                         # 'today'
print(humanize.naturalday(DT.datetime.now() - DT.timedelta(days=1)))  # 'yesterday'
print(humanize.naturalday(DT.date(2007, 6, 5)))                       # 'Jun 05'
print()

print(DT.timedelta(seconds=1001))                         # '0:16:41'
print(humanize.naturaldelta(DT.timedelta(seconds=1001)))  # '16 minutes'
print(humanize.naturaldelta(DT.timedelta(seconds=5)))     # '5 seconds'
print(humanize.naturaldelta(DT.timedelta(hours=30)))      # 'a day'
print(humanize.naturaldelta(DT.timedelta(hours=60)))      # '2 days'
print()

print(humanize.naturaldate(DT.date(2007, 6, 5)))  # 'Jun 05 2007'
print(humanize.naturaldate(DT.date(2007, 6, 5)))  # 'Jun 05 2007'
print()

print(humanize.naturaltime(DT.datetime.now() - DT.timedelta(seconds=1)))     # 'a second ago'
print(humanize.naturaltime(DT.datetime.now() - DT.timedelta(seconds=3600)))  # 'an hour ago'
print(humanize.naturaltime(DT.datetime.now() - DT.timedelta(hours=30)))      # 'a day ago'
print()


# File size humanization:
print(humanize.naturalsize(100))                   # '100 Bytes'
print(humanize.naturalsize(10 ** 9))               # '1.0 GB'
print(humanize.naturalsize(10 ** 9, binary=True))  # '953.7 MiB'
print(humanize.naturalsize(10 ** 9, gnu=True))     # '953.7M'
print()


# Localization
# How to change locale in runtime
print(humanize.naturaltime(DT.timedelta(seconds=3)))  # '3 seconds ago'
print(humanize.intword(123455913))      # '123.5 million'
print(humanize.intword(12345591313))    # '12.3 billion'
print(humanize.intword(1339014900000))  # '1.3 trillion'
print(humanize.apnumber(4))             # 'four'
print(humanize.apnumber(7))             # 'seven'
print()

_t = humanize.i18n.activate('ru_RU')

print(humanize.naturaltime(DT.timedelta(seconds=3)))  # '3 секунды назад'
print(humanize.intword(123455913))      # '123.5 миллиона'
print(humanize.intword(12345591313))    # '12.3 миллиарда'
print(humanize.intword(1339014900000))  # '1.3 триллиона'
print(humanize.apnumber(4))             # 'четыре'
print(humanize.apnumber(7))             # 'семь'
print()

humanize.i18n.deactivate()

print(humanize.naturaltime(DT.timedelta(seconds=3)))  # '3 seconds ago'
print(humanize.intword(123455913))      # '123.5 million'
print(humanize.intword(12345591313))    # '12.3 billion'
print(humanize.intword(1339014900000))  # '1.3 trillion'
print(humanize.apnumber(4))             # 'four'
print(humanize.apnumber(7))             # 'seven'
