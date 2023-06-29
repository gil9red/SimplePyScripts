#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/jmoiron/humanize


import datetime as dt

# pip install humanize
import humanize


# Date & time humanization
print(humanize.naturalday(dt.datetime.now()))  # 'today'
print(humanize.naturalday(dt.datetime.now() - dt.timedelta(days=1)))  # 'yesterday'
print(humanize.naturalday(dt.date(2007, 6, 5)))  # 'Jun 05'
print()

print(dt.timedelta(seconds=1001))  # '0:16:41'
print(humanize.naturaldelta(dt.timedelta(seconds=1001)))  # '16 minutes'
print(humanize.naturaldelta(dt.timedelta(seconds=5)))  # '5 seconds'
print(humanize.naturaldelta(dt.timedelta(hours=30)))  # 'a day'
print(humanize.naturaldelta(dt.timedelta(hours=60)))  # '2 days'
print()

print(humanize.naturaldate(dt.date(2007, 6, 5)))  # 'Jun 05 2007'
print(humanize.naturaldate(dt.date(2007, 6, 5)))  # 'Jun 05 2007'
print()

print(humanize.naturaltime(dt.datetime.now() - dt.timedelta(seconds=1)))
# 'a second ago'
print(humanize.naturaltime(dt.datetime.now() - dt.timedelta(seconds=3600)))
# 'an hour ago'
print(humanize.naturaltime(dt.datetime.now() - dt.timedelta(hours=30)))
# 'a day ago'
