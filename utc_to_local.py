#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime, timezone


# SOURCE: https://stackoverflow.com/a/13287083/5909792
def utc_to_local(utc_dt: datetime) -> datetime:
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


if __name__ == "__main__":
    dt_utc = datetime.strptime("2018-10-02T08:20:19.532Z", "%Y-%m-%dT%H:%M:%S.%fZ")
    dt_local = utc_to_local(dt_utc)

    print(dt_utc)  # 2018-10-02 08:20:19.532000
    print(dt_utc.strftime("%H:%M:%S"))  # 08:20:19
    print()

    print(dt_local)  # 2018-10-02 13:20:19.532000+05:00
    print(dt_local.strftime("%H:%M:%S"))  # 13:20:19
