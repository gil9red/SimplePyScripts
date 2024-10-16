#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
from datetime import timedelta
from enum import IntEnum


class UnitSeconds(IntEnum):
    SECOND = 1
    MINUTE = 60
    HOUR = 60 * MINUTE
    DAY = 24 * HOUR
    WEEK = 7 * DAY
    MONTH = 4 * WEEK
    YEAR = 12 * MONTH


@dataclass
class L10N:
    singular: dict[UnitSeconds, str]
    plural: dict[UnitSeconds, str]


L10N_EN = L10N(
    singular={
        UnitSeconds.SECOND: "{value} second ago",
        UnitSeconds.MINUTE: "{value} minute ago",
        UnitSeconds.HOUR: "{value} hour ago",
        UnitSeconds.DAY: "{value} day ago",
        UnitSeconds.WEEK: "{value} week ago",
        UnitSeconds.MONTH: "{value} month ago",
        UnitSeconds.YEAR: "{value} year ago",
    },
    plural={
        UnitSeconds.SECOND: "{value} seconds ago",
        UnitSeconds.MINUTE: "{value} minutes ago",
        UnitSeconds.HOUR: "{value} hours ago",
        UnitSeconds.DAY: "{value} days ago",
        UnitSeconds.WEEK: "{value} weeks ago",
        UnitSeconds.MONTH: "{value} months ago",
        UnitSeconds.YEAR: "{value} years ago",
    },
)


def ago(seconds: timedelta, l10n: L10N = L10N_EN) -> str:
    seconds = int(seconds.total_seconds())

    def _get_value_template(value: int, unit: UnitSeconds):
        return l10n.singular[unit] if value == 1 else l10n.plural[unit]

    for unit in sorted(UnitSeconds, reverse=True):
        value, seconds = divmod(seconds, unit)
        if value:
            template = _get_value_template(value, unit)
            return template.format(value=value)

    template = _get_value_template(seconds, UnitSeconds.SECOND)
    return template.format(value=seconds)


if __name__ == "__main__":
    from datetime import datetime

    dt = datetime(year=2024, month=12, day=12)

    items = [
        (timedelta(seconds=0), "0 seconds ago"),
        (timedelta(seconds=1), "1 second ago"),
        (timedelta(seconds=59), "59 seconds ago"),
        (timedelta(seconds=60), "1 minute ago"),
        (timedelta(seconds=90), "1 minute ago"),
        (timedelta(minutes=1), "1 minute ago"),
        (timedelta(minutes=5), "5 minutes ago"),
        (timedelta(minutes=45), "45 minutes ago"),
        (timedelta(hours=1, minutes=45), "1 hour ago"),
        (timedelta(hours=4, minutes=50), "4 hours ago"),
        (timedelta(hours=23, minutes=50), "23 hours ago"),
        (timedelta(hours=40, minutes=50), "1 day ago"),
        (timedelta(days=1), "1 day ago"),
        (timedelta(hours=48), "2 days ago"),
        (timedelta(days=2), "2 days ago"),
        (timedelta(days=7), "1 week ago"),
        (timedelta(days=8), "1 week ago"),
        (timedelta(weeks=1), "1 week ago"),
        (timedelta(weeks=2), "2 weeks ago"),
        (timedelta(weeks=4), "1 month ago"),
        (timedelta(weeks=8), "2 months ago"),
        (timedelta(weeks=12 * 4), "1 year ago"),
        (timedelta(weeks=5 * 12 * 4), "5 years ago"),
    ]
    for value, expected in items:
        actual = ago(dt - (dt - value))
        print(f"{value!r} -> {actual!r}")
        assert expected == actual, f"{expected!r} != {actual!r}"
