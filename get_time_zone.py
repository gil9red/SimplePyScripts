#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


if __name__ == "__main__":
    import dateutil.tz as dtz
    import pytz

    for name in pytz.common_timezones:
        print(dtz.gettz(name))
