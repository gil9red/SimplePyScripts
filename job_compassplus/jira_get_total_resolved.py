#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
from dataclasses import dataclass

from root_config import JIRA_HOST
from root_common import session


URL_SEARCH = f"{JIRA_HOST}/rest/api/latest/search"

JQL_RESOLUTION_DATE = "assignee = currentUser() AND resolutiondate"
JQL_TOTAL = f"{JQL_RESOLUTION_DATE} IS NOT EMPTY"
JQL_LAST_WEEK = f"{JQL_RESOLUTION_DATE} >= startOfDay(-7)"
JQL_LAST_MONTH = f"{JQL_RESOLUTION_DATE} >= startOfMonth(-1)"
JQL_LAST_YEAR = f"{JQL_RESOLUTION_DATE} >= startOfMonth(-12)"


@dataclass
class Stats:
    last_7_days: int
    last_month: int
    last_year: int
    total: int


def get_total(jql: str) -> int:
    query = {
        "jql": jql,
        "fields": "key",
        "maxResults": 0,
    }

    rs = session.get(URL_SEARCH, params=query)
    rs.raise_for_status()

    return rs.json()["total"]


def get_stats(sleep: float = 0.5) -> Stats:
    last_7_days = get_total(JQL_LAST_WEEK)
    time.sleep(sleep)

    last_month = get_total(JQL_LAST_MONTH)
    time.sleep(sleep)

    last_year = get_total(JQL_LAST_YEAR)
    time.sleep(sleep)

    total = get_total(JQL_TOTAL)

    return Stats(
        last_7_days=last_7_days,
        last_month=last_month,
        last_year=last_year,
        total=total,
    )


if __name__ == "__main__":
    print(get_stats())
