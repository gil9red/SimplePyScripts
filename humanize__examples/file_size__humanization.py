#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/jmoiron/humanize


# pip install humanize
import humanize


# File size humanization:
print(humanize.naturalsize(100))  # '100 Bytes'
print(humanize.naturalsize(10**9))  # '1.0 GB'
print(humanize.naturalsize(10**9, binary=True))  # '953.7 MiB'
print(humanize.naturalsize(10**9, gnu=True))  # '953.7M'
