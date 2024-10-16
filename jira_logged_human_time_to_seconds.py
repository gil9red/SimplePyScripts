#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from enum import IntEnum


class UnitSeconds(IntEnum):
    MINUTE = 60
    HOUR = 60 * MINUTE
    DAY = 8 * HOUR
    WEEK = 5 * DAY


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
        value, metric = part.upper().split()

        value = int(value)
        metric = metric.removesuffix("S")  # NOTE: "HOURS" -> "HOUR"

        total_seconds += value * UnitSeconds[metric]

    return total_seconds


def seconds_to_logged_human_time(seconds: int) -> str:
    weeks, seconds = divmod(seconds, UnitSeconds.WEEK)
    days, seconds = divmod(seconds, UnitSeconds.DAY)
    hours, seconds = divmod(seconds, UnitSeconds.HOUR)
    minutes, _ = divmod(seconds, UnitSeconds.MINUTE)

    get_suffix = lambda n: 's' if n > 1 else ''
    items = [
        f"{weeks} week{get_suffix(weeks)}" if weeks else '',
        f"{days} day{get_suffix(days)}" if days else '',
        f"{hours} hour{get_suffix(hours)}" if hours else '',
        f"{minutes} minute{get_suffix(minutes)}" if minutes else '',
    ]
    return ", ".join(filter(None, items))


if __name__ == "__main__":
    items = [
        ("2 hours", 2 * 60 * 60),
        ("1 hour, 15 minutes", 3600 + 15 * 60),
        ("1 hour, 30 minutes", 3600 + 1800),
        ("4 hours", 4 * 3600),
        ("7 hours", 7 * 3600),
        ("1 day, 1 hour", 8 * 3600 + 3600),
        ("6 hours, 30 minutes", 6 * 3600 + 1800),
        ("30 minutes", 30 * 60),
        ("1 day", 8 * 3600),
        ("1 hour", 3600),
        ("4 hours, 30 minutes", 4 * 3600 + 1800),
        ("40 minutes", 40 * 60),
        ("45 minutes", 45 * 60),
        ("7 hours, 30 minutes", 7 * 3600 + 1800),
        ("1 day, 30 minutes", 8 * 3600 + 1800),
        ("5 hours", 5 * 3600),
        ("5 hours, 30 minutes", 5 * 3600 + 1800),
        ("1 minute", 60),
        ("1 hour, 20 minutes", 3600 + 20 * 60),
        ("6 hours", 6 * 3600),
        ("3 hours, 30 minutes", 3 * 3600 + 1800),
        ("15 minutes", 15 * 60),
        ("3 hours", 3 * 3600),
        ("1 week", 5 * 8 * 3600),
        (
            "1 week, 2 days, 1 hour",
            logged_human_time_to_seconds("5 day")
            + logged_human_time_to_seconds("2 day")
            + logged_human_time_to_seconds("1 hour")
        ),
    ]
    for value, expected in items:
        seconds = logged_human_time_to_seconds(value)
        print(f"{value!r} -> {seconds} seconds")
        assert expected == seconds

        logged_human = seconds_to_logged_human_time(seconds)
        print(f"{seconds} seconds -> {logged_human!r}")
        assert value == logged_human

        print()

    assert logged_human_time_to_seconds("1 day") == logged_human_time_to_seconds("8 hours")
    assert logged_human_time_to_seconds("5 days") == logged_human_time_to_seconds("1 week")

    value = "1 day, 4 hours, 15 minutes"
    assert seconds_to_logged_human_time(logged_human_time_to_seconds(value)) == value
