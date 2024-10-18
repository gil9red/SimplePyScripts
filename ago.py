#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


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


class L10N:
    def get_template(self) -> str:
        return "{value} {unit} ago"

    def get_unit(self, value: int, unit: UnitSeconds) -> str:
        unit = unit.name.lower()
        if value != 1:
            unit = f"{unit}s"
        return unit

    def get_value(self, value: int, unit: UnitSeconds) -> str:
        unit = self.get_unit(value, unit)
        return self.get_template().format(value=value, unit=unit)


class L10N_RU(L10N):
    def get_template(self) -> str:
        return "{value} {unit} назад"

    # SOURCE: https://ru.stackoverflow.com/a/1380460/201445
    @staticmethod
    def declension(n: int, form_0: str, form_1: str, form_2: str) -> str:
        units = n % 10
        tens = (n // 10) % 10
        if tens == 1:
            return form_0
        if units in [0, 5, 6, 7, 8, 9]:
            return form_0
        if units == 1:
            return form_1
        if units in [2, 3, 4]:
            return form_2

    def get_unit(self, value: int, unit: UnitSeconds) -> str:
        match unit:
            case UnitSeconds.SECOND:
                return self.declension(value, "секунд", "секунда", "секунды")

            case UnitSeconds.MINUTE:
                return self.declension(value, "минут", "минута", "минуты")

            case UnitSeconds.HOUR:
                return self.declension(value, "часов", "час", "часа")

            case UnitSeconds.DAY:
                return self.declension(value, "дней", "день", "дня")

            case UnitSeconds.WEEK:
                return self.declension(value, "недель", "неделя", "недели")

            case UnitSeconds.MONTH:
                return self.declension(value, "месяцев", "месяц", "месяца")

            case UnitSeconds.YEAR:
                return self.declension(value, "лет", "год", "года")

            case _:
                raise NotImplemented()


def ago(seconds: timedelta, l10n: L10N = L10N()) -> str:
    seconds = int(seconds.total_seconds())
    if seconds < 0:
        seconds = -seconds

    for unit in sorted(UnitSeconds, reverse=True):
        value, seconds = divmod(seconds, unit)
        if value:
            return l10n.get_value(value, unit)

    return l10n.get_value(seconds, UnitSeconds.SECOND)


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

    dt2 = datetime(year=2024, month=12, day=10)
    assert ago(dt2 - dt) == "2 days ago"

    print("\n" + "-" * 10 + "\n")

    items = [
        (timedelta(seconds=0), "0 секунд назад"),
        (timedelta(seconds=1), "1 секунда назад"),
        (timedelta(seconds=59), "59 секунд назад"),
        (timedelta(seconds=60), "1 минута назад"),
        (timedelta(seconds=90), "1 минута назад"),
        (timedelta(minutes=1), "1 минута назад"),
        (timedelta(minutes=5), "5 минут назад"),
        (timedelta(minutes=45), "45 минут назад"),
        (timedelta(hours=1, minutes=45), "1 час назад"),
        (timedelta(hours=4, minutes=50), "4 часа назад"),
        (timedelta(hours=23, minutes=50), "23 часа назад"),
        (timedelta(hours=40, minutes=50), "1 день назад"),
        (timedelta(days=1), "1 день назад"),
        (timedelta(hours=48), "2 дня назад"),
        (timedelta(days=2), "2 дня назад"),
        (timedelta(days=7), "1 неделя назад"),
        (timedelta(days=8), "1 неделя назад"),
        (timedelta(weeks=1), "1 неделя назад"),
        (timedelta(weeks=2), "2 недели назад"),
        (timedelta(weeks=4), "1 месяц назад"),
        (timedelta(weeks=8), "2 месяца назад"),
        (timedelta(weeks=12 * 4), "1 год назад"),
        (timedelta(weeks=5 * 12 * 4), "5 лет назад"),
    ]
    for value, expected in items:
        actual = ago(dt - (dt - value), l10n=L10N_RU())
        print(f"{value!r} -> {actual!r}")
        assert expected == actual, f"{expected!r} != {actual!r}"

    dt2 = datetime(year=2024, month=12, day=10)
    assert ago(dt2 - dt, l10n=L10N_RU()) == "2 дня назад"
