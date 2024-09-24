#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def logged_human_time_to_seconds(human_time: str) -> int:
    """Конвертирование человеко-читаемого времени в секунды.

    >>> logged_human_time_to_seconds("1 minute")
    60
    >>> logged_human_time_to_seconds("1 hour")
    3600
    >>> logged_human_time_to_seconds("6 hours, 30 minutes")
    23400
    >>> logged_human_time_to_seconds("1 day, 30 minutes")
    30600
    """

    # Jira help:
    #   You can specify a time unit after a time value 'X', such as Xw, Xd, Xh or Xm, to represent weeks (w),
    #   days (d), hours (h) and minutes (m), respectively.
    #   If you do not specify a time unit, minute will be assumed.
    #   Your current conversion rates are 1w = 5d and 1d = 8h.

    total_seconds = 0

    for part in human_time.split(", "):
        value, metric = part.lower().split()
        value = int(value)

        if "minute" in metric:
            total_seconds += value * 60

        elif "hour" in metric:
            total_seconds += value * 60 * 60

        elif "day" in metric:
            total_seconds += value * 8 * 60 * 60

        elif "week" in metric:
            total_seconds += value * 5 * 8 * 60 * 60

    return total_seconds


if __name__ == "__main__":
    text = """\
2 hours
1 hour, 30 minutes
4 hours
7 hours
1 day, 1 hour
6 hours, 30 minutes
30 minutes
1 day
1 hour
4 hours, 30 minutes
40 minutes
7 hours, 30 minutes
1 day, 30 minutes
5 hours
5 hours, 30 minutes
1 minute
1 hour, 20 minutes
6 hours
3 hours, 30 minutes
15 minutes
3 hours
"""

    for line in list(set(text.splitlines())):
        print(line, logged_human_time_to_seconds(line))

    assert logged_human_time_to_seconds("1 day") == logged_human_time_to_seconds("8 hours")
    assert logged_human_time_to_seconds("5 days") == logged_human_time_to_seconds("1 week")
