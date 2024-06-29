#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import re


# NOTE: Fix https://github.com/pallets/werkzeug/blob/72b2e48e7d44927b1b7d6b2f940d0691230de893/src/werkzeug/serving.py#L425C38-L425C44
class FilterRemoveDateFromWerkzeugLogs(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # "192.168.0.102 - - [30/Jun/2024 01:14:03] "%s" %s %s" -> "192.168.0.102 - "%s" %s %s"
        record.msg = re.sub(r' - - \[.+?] "', ' - "', record.msg)
        return True
