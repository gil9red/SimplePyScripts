#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from collections import defaultdict
from datetime import date

from api.common import Playlist, seconds_to_str


items: list[tuple[date, int]] = []

playlist = Playlist.get_from(
    "https://www.youtube.com/playlist?list=PLVOZT4ssBLx7PcRyXhtaymKyoqXQsEMVR"
)
for video in playlist.video_list:
    if video.is_lasy:
        video = video.get_from(video.id)

    items.append((video.create_date, video.duration_seconds))

items.sort(key=lambda x: x[0])

year_by_values: dict[int, list[tuple[date, int]]] = defaultdict(list)
for create_date, duration_seconds in items:
    year_by_values[create_date.year].append((create_date, duration_seconds))

last_date: date | None = None
for year, values in year_by_values.items():
    number = len(values)
    print(f"{year}. Video: {number}")

    dates: list[date] = []
    durations: list[int] = []

    for d, duration in values:
        delta_prev: int = (d - last_date).days if last_date else 0
        last_date = d

        print(f"    {d}: {seconds_to_str(duration)} [delta {delta_prev} days]")

        dates.append(d)
        durations.append(duration)

    print()

    delta_days: list[int] = [(b - a).days for a, b in zip(dates, dates[1::])]

    print(
        f"    Durations (total / min / max / mean): "
        f"{seconds_to_str(sum(durations))} "
        f"/ {seconds_to_str(min(durations))} "
        f"/ {seconds_to_str(max(durations))} "
        f"/ {seconds_to_str(sum(durations) // number)}\n"
        f"    Delta days (min / max / mean): "
        f"{min(delta_days)} "
        f"/ {max(delta_days)} "
        f"/ {sum(delta_days) // number}\n"
    )
"""
2018. Video: 3
    2018-09-21: 00:07:43 [delta 0 days]
    2018-10-25: 00:07:47 [delta 34 days]
    2018-12-07: 00:17:08 [delta 43 days]

    Durations (total / min / max / mean): 00:32:38 / 00:07:43 / 00:17:08 / 00:10:52
    Delta days (min / max / mean): 34 / 43 / 25

2019. Video: 22
    2019-01-11: 00:15:31 [delta 35 days]
    2019-02-02: 00:18:47 [delta 22 days]
    2019-02-17: 00:11:28 [delta 15 days]
    2019-03-30: 00:23:33 [delta 41 days]
    2019-04-19: 00:12:16 [delta 20 days]
    2019-05-04: 00:14:16 [delta 15 days]
    2019-05-27: 00:26:27 [delta 23 days]
    2019-06-09: 00:09:36 [delta 13 days]
    2019-06-20: 00:12:56 [delta 11 days]
    2019-07-05: 00:16:34 [delta 15 days]
    2019-07-21: 00:13:20 [delta 16 days]
    2019-08-02: 00:10:51 [delta 12 days]
    2019-08-16: 00:11:39 [delta 14 days]
    2019-08-31: 00:10:23 [delta 15 days]
    2019-09-14: 00:10:27 [delta 14 days]
    2019-09-27: 00:16:28 [delta 13 days]
    2019-10-20: 00:19:28 [delta 23 days]
    2019-11-03: 00:19:04 [delta 14 days]
    2019-11-17: 00:16:39 [delta 14 days]
    2019-12-10: 00:15:54 [delta 23 days]
    2019-12-15: 00:07:57 [delta 5 days]
    2019-12-30: 00:18:45 [delta 15 days]

    Durations (total / min / max / mean): 05:32:19 / 00:07:57 / 00:26:27 / 00:15:06
    Delta days (min / max / mean): 5 / 41 / 16

2020. Video: 20
    2020-01-13: 00:20:14 [delta 14 days]
    2020-02-04: 00:27:15 [delta 22 days]
    2020-02-21: 00:17:02 [delta 17 days]
    2020-03-01: 00:10:47 [delta 9 days]
    2020-03-22: 00:10:24 [delta 21 days]
    2020-04-06: 00:18:05 [delta 15 days]
    2020-04-19: 00:13:31 [delta 13 days]
    2020-05-02: 00:15:36 [delta 13 days]
    2020-05-15: 00:12:05 [delta 13 days]
    2020-06-03: 00:16:13 [delta 19 days]
    2020-06-17: 00:17:17 [delta 14 days]
    2020-07-01: 00:13:16 [delta 14 days]
    2020-07-19: 00:19:48 [delta 18 days]
    2020-08-08: 00:18:45 [delta 20 days]
    2020-08-25: 00:13:55 [delta 17 days]
    2020-09-20: 00:23:36 [delta 26 days]
    2020-10-09: 00:27:34 [delta 19 days]
    2020-10-29: 00:22:34 [delta 20 days]
    2020-11-23: 00:33:18 [delta 25 days]
    2020-12-26: 00:27:40 [delta 33 days]

    Durations (total / min / max / mean): 06:18:55 / 00:10:24 / 00:33:18 / 00:18:56
    Delta days (min / max / mean): 9 / 33 / 17

2021. Video: 13
    2021-01-30: 00:36:57 [delta 35 days]
    2021-02-21: 00:18:08 [delta 22 days]
    2021-03-26: 00:25:44 [delta 33 days]
    2021-04-25: 00:20:05 [delta 30 days]
    2021-05-23: 00:25:11 [delta 28 days]
    2021-06-05: 00:11:38 [delta 13 days]
    2021-07-03: 00:21:41 [delta 28 days]
    2021-08-07: 00:33:33 [delta 35 days]
    2021-08-29: 00:13:30 [delta 22 days]
    2021-09-26: 00:23:49 [delta 28 days]
    2021-10-16: 00:25:37 [delta 20 days]
    2021-11-21: 00:51:54 [delta 36 days]
    2021-12-25: 00:30:30 [delta 34 days]

    Durations (total / min / max / mean): 05:38:17 / 00:11:38 / 00:51:54 / 00:26:01
    Delta days (min / max / mean): 13 / 36 / 25

2022. Video: 9
    2022-01-26: 00:33:07 [delta 32 days]
    2022-02-20: 00:24:41 [delta 25 days]
    2022-04-09: 00:32:01 [delta 48 days]
    2022-05-24: 00:31:31 [delta 45 days]
    2022-07-03: 00:45:53 [delta 40 days]
    2022-07-30: 00:24:29 [delta 27 days]
    2022-09-14: 00:33:14 [delta 46 days]
    2022-10-25: 00:32:45 [delta 41 days]
    2022-12-01: 00:37:55 [delta 37 days]

    Durations (total / min / max / mean): 04:55:36 / 00:24:29 / 00:45:53 / 00:32:50
    Delta days (min / max / mean): 25 / 48 / 34

2023. Video: 7
    2023-01-03: 00:22:37 [delta 33 days]
    2023-02-17: 00:55:16 [delta 45 days]
    2023-03-17: 00:24:09 [delta 28 days]
    2023-05-16: 01:04:21 [delta 60 days]
    2023-07-19: 00:53:27 [delta 64 days]
    2023-09-11: 00:37:31 [delta 54 days]
    2023-11-07: 00:59:13 [delta 57 days]

    Durations (total / min / max / mean): 05:16:34 / 00:22:37 / 01:04:21 / 00:45:13
    Delta days (min / max / mean): 28 / 64 / 44

2024. Video: 6
    2024-01-09: 01:12:18 [delta 63 days]
    2024-03-11: 00:52:00 [delta 62 days]
    2024-05-10: 00:54:33 [delta 60 days]
    2024-07-09: 00:51:58 [delta 60 days]
    2024-08-30: 00:54:57 [delta 52 days]
    2024-11-11: 01:29:10 [delta 73 days]

    Durations (total / min / max / mean): 06:14:56 / 00:51:58 / 01:29:10 / 01:02:29
    Delta days (min / max / mean): 52 / 73 / 51
"""
