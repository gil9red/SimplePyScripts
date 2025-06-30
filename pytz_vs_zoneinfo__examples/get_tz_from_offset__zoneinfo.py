#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from datetime import datetime, timedelta, timezone, tzinfo


PATTERN_TZ_OFFSET = re.compile(r"(?P<sign>[+-])(?P<hour>\d{2}):?(?P<minute>\d{2})")


def get_tz(value: str) -> tzinfo:
    m = PATTERN_TZ_OFFSET.search(value)
    if not m:
        raise Exception(f"Invalid time zone: {value!r}")

    sign: str = m.group("sign")
    hour: int = int(m.group("hour"))
    minute: int = int(m.group("minute"))

    total_minutes = hour * 60 + minute
    if sign == "-":
        total_minutes = -total_minutes

    return timezone(offset=timedelta(minutes=total_minutes))


if __name__ == "__main__":
    import zoneinfo

    now_utc = datetime.utcnow()

    tz_etc_0300 = zoneinfo.ZoneInfo("Etc/GMT-3")
    print(now_utc.astimezone(tz_etc_0300).strftime("%z"))
    # +0300

    tz_offset_0300 = timezone(offset=timedelta(minutes=3 * 60))
    print(now_utc.astimezone(tz_offset_0300).strftime("%z"))
    # +0300

    print(now_utc.astimezone(get_tz("+0300")).strftime("%z"))
    # +0300

    print(now_utc.astimezone(get_tz("+03:00")).strftime("%z"))
    # +0300

    print(now_utc.astimezone(get_tz("-0300")).strftime("%z"))
    # -0300
