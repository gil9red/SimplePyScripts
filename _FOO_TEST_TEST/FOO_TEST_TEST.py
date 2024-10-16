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
    MONTH = 30 * DAY  # NOTE: 4 * WEEK = ~28 days in year
    YEAR = 12 * MONTH


@dataclass
class L18N:
    singular: dict[UnitSeconds, str]
    plural: dict[UnitSeconds, str]


L18N_EN = L18N(
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


def ago(seconds: timedelta, l18n: L18N = L18N_EN) -> str:
    seconds = int(seconds.total_seconds())

    def _get_value_template(value: int, unit: UnitSeconds):
        return l18n.plural[unit] if value > 1 else l18n.singular[unit]

    for unit in sorted(UnitSeconds, reverse=True):
        value, seconds = divmod(seconds, unit)
        if value:
            template = _get_value_template(value, unit)
            return template.format(value=value)

    raise Exception(f"Unsupported: {seconds}")


if __name__ == "__main__":
    from datetime import datetime
    print(ago(datetime(year=2024, month=12, day=12) - datetime(year=2024, month=12, day=10)))
