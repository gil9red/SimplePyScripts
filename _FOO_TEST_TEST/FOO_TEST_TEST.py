#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# from PyQt5.QtWidgets import QApplication, QTextBrowser
#
#
# app = QApplication([])
#
# mw = QTextBrowser()
# mw.setHtml("""
# <style>
#     #test {
#         color: red;
#         font-size: 30px;
#     }
# </style>
# <div id="test">Test<div>
#
# <script>
#     document.getElementById("test").style.color = "blue";
# </script>
# """)
# mw.show()
#
# app.exec()
#
#
# quit()


from dataclasses import dataclass, field
from datetime import datetime, timedelta, date


def add_to_month(d: date, inc: bool = True, number: int = 1) -> date:
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

26, 11.01.2022, 14.03.2022, 15.11.2022 +8, 

27, 03.03.2022, 27.05.2022, 09.12.2022 +7, +1
28, 05.05.2022, 15.07.2022, 10.02.2023 +7, +2
29, 04.07.2022, 15.09.2022, 24.05.2023 +8, +3

30, 01.09.2022, 15.11.2022, 05.06.2023 +7, +1
31, 01.11.2023, 19.01.2023, 01.08.2023 +7, +2
32, 09.01.2023, 14.03.2023, 07.11.2023 +8, +3

33, 02.03.2023, 18.05.2023, 04.12.2023 +7, +1
34, 04.05.2023, 21.07.2023, 01.02.2024 +7, +2
35, 05.07.2023, 15.09.2023, 03.05.2024 +8, +3

36, 04.09.2023, 21.11.2023, 07.06.2024 +7, +1
37, 02.11.2023, 23.01.2024, 05.08.2024 +7, +2
38, 11.01.2024, 15.03.2024, 28.11.2024 +8, +3
"""


INIT_RELEASE_VERSION: int = 31
INIT_RELEASE_DATE: date = date(year=2022, month=11, day=1)


@dataclass
class Release:
    version: int
    date: date
    free_commit_date: date = field(init=False)
    testing_finish_date: date = field(init=False)
    support_end_date: date = field(init=False)

    def __post_init__(self):
        self.free_commit_date = add_to_month(self.date, number=1) - timedelta(days=1)
        self.testing_finish_date = add_to_month(self.date, number=2)
        self.support_end_date = add_to_month(
            self.testing_finish_date,
            # NOTE: Месяца 3 и 9, похоже, связаны с IPS mandates
            number=8 if self.testing_finish_date.month in (3, 9) else 7,
        )

    @classmethod
    def get_by(cls, d: date = None, version: int = None) -> "Release":
        if d is None and version is None:
            # TODO: Нормальное исключение
            raise Exception()

        if d is not None:
            _is_found = lambda r: r.date <= d < r.testing_finish_date
        else:
            _is_found = lambda r: r.version == version

        if d is not None:
            _is_need_next = lambda r: d > r.date
        else:
            _is_need_next = lambda r: version > r.version

        release = Release(
            version=INIT_RELEASE_VERSION,
            date=INIT_RELEASE_DATE,
        )

        while True:
            if _is_found(release):
                return release

            release = (
                release.get_next_release()
                if _is_need_next(release)
                else release.get_prev_release()
            )

        return release

    @classmethod
    def get_by_date(cls, d: date) -> "Release":
        return cls.get_by(d=d)

    @classmethod
    def get_by_version(cls, version: int) -> "Release":
        return cls.get_by(version=version)

    @classmethod
    def get_last_release(cls) -> "Release":
        return cls.get_by_date(date.today())

    def get_next_release(self) -> "Release":
        return Release(
            version=self.version + 1,
            date=add_to_month(self.date, number=2),
        )

    def get_prev_release(self) -> "Release":
        return Release(
            version=self.version - 1,
            date=add_to_month(self.date, inc=False, number=2),
        )

    def is_last_release(self) -> bool:
        return self == self.get_last_release()


last_release: Release = Release.get_last_release()
print("last_release:", last_release)

releases: list[Release] = [
    Release.get_by_version(version)
    for version in range(last_release.version - 6, last_release.version + 6 + 1)
]
for release in releases:
    print(release, release.is_last_release())


# for _ in range(15):
#     release = releases[-1]
#     releases.append(release.get_next_release())


# TODO: В тесты
# release = releases[-1]
# releases_v2 = [release]
# for _ in range(15):
#     release = release.get_prev_release()
#     releases_v2.append(release)
# print(releases_v2 == releases)
#
# for r1, r2 in zip(releases, releases_v2[::-1]):
#     print(r1 == r2)
#     print(f"{r1}\n{r2}")
#     print()

# for r in releases:
#     print(r)


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
