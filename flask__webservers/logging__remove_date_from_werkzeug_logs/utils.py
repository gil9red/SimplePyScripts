#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import re


class FilterRemoveDateFromWerkzeugLogs(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # "192.168.0.102 - - [30/Jun/2024 01:14:03] "%s" %s %s" -> "192.168.0.102 - "%s" %s %s"
        record.msg = re.sub(r' - - \[.+?] "', ' - "', record.msg)
        return True
