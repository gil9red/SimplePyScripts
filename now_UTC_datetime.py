#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime, timezone

utc_datetime_old = datetime.utcnow().replace(microsecond=0)
print(utc_datetime_old)

utc_datetime = datetime.now(timezone.utc).replace(microsecond=0)
print(utc_datetime)

assert utc_datetime_old != utc_datetime
assert utc_datetime_old == utc_datetime.replace(tzinfo=None)
