#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/jmoiron/humanize

import datetime as DT

# pip install humanize
import humanize


# Date & time humanization
print(humanize.naturalday(DT.datetime.now()))  # 'today'
print(humanize.naturalday(DT.datetime.now() - DT.timedelta(days=1)))  # 'yesterday'
print(humanize.naturalday(DT.date(2007, 6, 5)))  # 'Jun 05'
print()

print(DT.timedelta(seconds=1001))  # '0:16:41'
print(humanize.naturaldelta(DT.timedelta(seconds=1001)))  # '16 minutes'
print(humanize.naturaldelta(DT.timedelta(seconds=5)))  # '5 seconds'
print(humanize.naturaldelta(DT.timedelta(hours=30)))  # 'a day'
print(humanize.naturaldelta(DT.timedelta(hours=60)))  # '2 days'
print()

print(humanize.naturaldate(DT.date(2007, 6, 5)))  # 'Jun 05 2007'
print(humanize.naturaldate(DT.date(2007, 6, 5)))  # 'Jun 05 2007'
print()

print(humanize.naturaltime(DT.datetime.now() - DT.timedelta(seconds=1)))
# 'a second ago'
print(humanize.naturaltime(DT.datetime.now() - DT.timedelta(seconds=3600)))
# 'an hour ago'
print(humanize.naturaltime(DT.datetime.now() - DT.timedelta(hours=30)))
# 'a day ago'
