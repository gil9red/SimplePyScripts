#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/f0403620f7948306ad9e34a373f2aabc0237fb2a/seconds_to_str.py
def seconds_to_str(seconds: int) -> str:
    hh, mm = divmod(seconds, 3600)
    mm, ss = divmod(mm, 60)
    return "%02d:%02d:%02d" % (hh, mm, ss)


def time_to_seconds(time_str: str) -> int:
    time_split = list(map(int, time_str.split(':')))

    if len(time_split) == 3:
        h, m, s = time_split
        return h * 60 * 60 + m * 60 + s

    elif len(time_split) == 2:
        m, s = time_split
        return m * 60 + s

    else:
        return time_split[0]
