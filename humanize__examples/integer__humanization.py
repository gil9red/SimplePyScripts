#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/jmoiron/humanize


# pip install humanize
import humanize


# Integer humanization:
print(humanize.intcomma(12345))  # '12,345'
print(humanize.intcomma(123456789))  # '123,456,789'
print()

print(humanize.intword(123455913))  # '123.5 million'
print(humanize.intword(12345591313))  # '12.3 billion'
print(humanize.intword(1339014900000))  # '1.3 trillion'
print()

print(humanize.apnumber(4))  # 'four'
print(humanize.apnumber(7))  # 'seven'
print(humanize.apnumber(41))  # '41'
