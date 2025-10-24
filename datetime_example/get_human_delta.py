#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import timedelta, datetime


def get_human_delta(delta: timedelta) -> str:
    days = delta.days

    seconds_remainder = delta.seconds
    hours, seconds_remainder = divmod(seconds_remainder, 3600)
    minutes, seconds = divmod(seconds_remainder, 60)

    years, days = divmod(days, 365)
    lines: list[str] = []
    if years > 0:
        lines.append(f"{years} year{'s' if years > 1 else ''}")

    if days > 0:
        lines.append(f"{days} day{'s' if days > 1 else ''}")

    lines.append(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    return ", ".join(lines)


if __name__ == "__main__":
    for expected, delta in [
        ("00:00:05", timedelta(seconds=5)),
        ("02:30:00", timedelta(hours=2, minutes=30, seconds=0)),
        ("02:30:00", timedelta(hours=2, minutes=30, seconds=0, microseconds=777)),
        ("1 day, 02:30:00", timedelta(days=1, hours=2, minutes=30, seconds=0)),
        ("2 days, 02:30:00", timedelta(days=2, hours=2, minutes=30, seconds=0)),
        ("1 year, 35 days, 02:01:00", timedelta(days=400, hours=2, minutes=1)),
        ("2 years, 170 days, 02:01:00", timedelta(days=900, hours=2, minutes=1)),
    ]:
        human_delta: str = get_human_delta(delta)
        print(human_delta)
        assert expected == human_delta
