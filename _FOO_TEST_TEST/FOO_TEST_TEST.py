#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
from datetime import datetime, timedelta, date


def change_month(d: date, inc: bool = True, number: int = 1) -> date:
    d = d.replace(day=1)

    year = d.year
    month = d.month

    for _ in range(number):
        month += 1 if inc else -1
        if month > 12:
            month = 1
            year += 1
        elif month < 1:
            month = 12
            year -= 1

        d = date(year=year, month=month, day=1)

    return d


"""
Date: 06 мая 2024 г. 21:11:42 | Release version 3.2.40.10 (release based on revision 324264)
Date: 03 июля 2024 г. 19:11:35 | Release version 3.2.41.10 (release based on revision 327113)
Date: 04 сентября 2024 г. 15:08:49 | Release version 3.2.42.10 (release based on revision 330920)
Date: 05 ноября 2024 г. 19:40:28 | Release version 3.2.43.10 (release based on revision 335027)
"""


@dataclass
class Release:
    date: date
    version: int
    # TODO: Дата + месяц, когда можно коммитить без согласования
    # TODO: Дата окончания поддержки
    # TODO: post_init

    def get_next_release(self) -> "Release":
        return Release(
            date=change_month(self.date, number=2),
            version=self.version + 1,
        )


releases: list[Release] = [
    Release(
        date=date.today().replace(month=5, day=1),
        version=40,
    ),
]

for _ in range(10):
    release = releases[-1]
    releases.append(release.get_next_release())
    print(releases[-1])

# d = date.today().replace(day=1)
# print(d)
# print()
#
# for _ in range(20):
#     d = change_month(d)
#     print(d)


quit()


def get_zero_time(dt: datetime) -> datetime:
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


# TODO: date
def get_items(
    start_dt: datetime,
    end_dt: datetime,
    delta: timedelta,
) -> list[tuple[datetime, datetime]]:
    items = []

    dt = end_dt
    while True:
        if dt <= start_dt:
            break

        dt1 = dt
        dt -= delta

        if dt < start_dt:
            dt = start_dt

        items.append((dt, dt1))

    return items


# TODO: date
def to_ms(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)


# TODO: date
dt = get_zero_time(datetime.utcnow())
print(dt)
# 2024-12-04 00:00:00

for dt1, dt2 in get_items(
    start_dt=get_zero_time(dt - timedelta(weeks=6)),
    end_dt=get_zero_time(dt + timedelta(days=1)),
    delta=timedelta(weeks=1),
):
    print(f"{dt1} - {dt2}. {to_ms(dt1)}+{to_ms(dt2)}")
"""
2024-11-28 00:00:00 - 2024-12-05 00:00:00. 1732734000000+1733338800000
2024-11-21 00:00:00 - 2024-11-28 00:00:00. 1732129200000+1732734000000
2024-11-14 00:00:00 - 2024-11-21 00:00:00. 1731524400000+1732129200000
2024-11-07 00:00:00 - 2024-11-14 00:00:00. 1730919600000+1731524400000
2024-10-31 00:00:00 - 2024-11-07 00:00:00. 1730314800000+1730919600000
2024-10-24 00:00:00 - 2024-10-31 00:00:00. 1729710000000+1730314800000
2024-10-23 00:00:00 - 2024-10-24 00:00:00. 1729623600000+1729710000000
"""
