#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/jmoiron/humanize


import datetime as DT

# pip install humanize
import humanize


# Localization. How to change locale in runtime
print(humanize.naturaltime(DT.timedelta(seconds=3)))  # '3 seconds ago'
print(humanize.intword(123455913))  # '123.5 million'
print(humanize.intword(12345591313))  # '12.3 billion'
print(humanize.intword(1339014900000))  # '1.3 trillion'
print(humanize.apnumber(4))  # 'four'
print(humanize.apnumber(7))  # 'seven'
print()

_t = humanize.i18n.activate("ru_RU")

print(humanize.naturaltime(DT.timedelta(seconds=3)))  # '3 секунды назад'
print(humanize.intword(123455913))  # '123.5 миллиона'
print(humanize.intword(12345591313))  # '12.3 миллиарда'
print(humanize.intword(1339014900000))  # '1.3 триллиона'
print(humanize.apnumber(4))  # 'четыре'
print(humanize.apnumber(7))  # 'семь'
print()

humanize.i18n.deactivate()

print(humanize.naturaltime(DT.timedelta(seconds=3)))  # '3 seconds ago'
print(humanize.intword(123455913))  # '123.5 million'
print(humanize.intword(12345591313))  # '12.3 billion'
print(humanize.intword(1339014900000))  # '1.3 trillion'
print(humanize.apnumber(4))  # 'four'
print(humanize.apnumber(7))  # 'seven'
