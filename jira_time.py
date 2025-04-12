#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

from collections import defaultdict
from datetime import datetime


def seconds_to_jira_str(seconds: int) -> str:
    hours, minutes = divmod(seconds, 3600)
    minutes //= 60
    days, hours = divmod(hours, 8)
    weeks, days = divmod(days, 5)

    items = [
        f"{weeks}w" if weeks else "",
        f"{days}d" if days else "",
        f"{hours}h" if hours else "",
        f"{minutes}m" if minutes else "",
    ]
    return " ".join(filter(None, items))


def str_to_time(s: str) -> datetime:
    return datetime.strptime(s, "%H:%M")


def parser_my_jira_time_logs(log: str) -> str:
    pattern = re.compile(r"(.+) (\d\d:\d\d)-(\d\d:\d\d)")

    jira_by_seconds: dict[str, int] = defaultdict(int)

    for line in log.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        m = pattern.match(line)

        jira: str = m.group(1)
        t1: str = m.group(2)
        t2: str = m.group(3)
        seconds: int = (str_to_time(t2) - str_to_time(t1)).seconds

        jira_by_seconds[jira] += seconds

    return "\n".join(
        f"{jira}: {seconds_to_jira_str(seconds)}"
        for jira, seconds in jira_by_seconds.items()
    )


if __name__ == "__main__":
    print(
        parser_my_jira_time_logs(
            """
            # Foo
            7417 10:00-18:00
    
            # Bar
            7417 10:00-12:00
            7417 12:19-14:00
            7417 14:37-15:30
            7417 15:58-17:50
    
            7415 15:58-15:59
            7456 14:28-15:59
            7425 10:00-18:10
            """
        )
    )
    """
    7417: 1d 6h 26m
    7415: 1m
    7456: 1h 31m
    77425: 1d 10m
    """
