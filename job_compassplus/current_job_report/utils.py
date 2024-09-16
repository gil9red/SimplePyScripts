#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as dt
import sys

from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))
from root_common import session

sys.path.append(str(DIR.parent.parent))
from get_quarter import (
    get_quarter_num,
    get_quarter_roman,  # NOTE: оставить get_quarter_roman для main.py
)


class NotFoundReport(Exception):
    pass


URL = "https://helpdesk.compassluxe.com/pa-reports/"


def _send_data(data: dict) -> str:
    # В какой-то момент адрес временно поменялся, тогда предварительный GET поможет получить актуальный адрес
    rs = session.get(URL)
    if not rs.ok:
        raise NotFoundReport(f"HTTP status is {rs.status_code}")

    rs = session.post(rs.url, data=data)
    if not rs.ok:
        raise NotFoundReport(f"HTTP status is {rs.status_code}")

    return rs.text


def get_report_context() -> str:
    today = dt.datetime.today()
    data = {
        "dep": "all",
        "rep": "rep1",
        "period": today.strftime("%Y-%m"),
        "v": int(today.timestamp() * 1000),
        "type": "normal",
    }
    return _send_data(data)


def get_quarter_report_context() -> str:
    today = dt.datetime.today()
    data = {
        "dep": "all",
        "rep": "rep1",
        "quarter": "quarter",
        "period": f"{today.year}-q{get_quarter_num(today)}",
        "v": int(today.timestamp() * 1000),
        "type": "normal",
    }
    return _send_data(data)


def get_year_report_context() -> str:
    today = dt.datetime.today()
    data = {
        "dep": "all",
        "rep": "rep1",
        "toMonth": "12",
        "total": "total",
        "quarter": "quarter",
        "period": f"{today.year}-p01-12",
        "v": int(today.timestamp() * 1000),
        "type": "normal",
    }
    return _send_data(data)


if __name__ == "__main__":
    dt = dt.datetime.now()
    print(dt, get_quarter_num(dt), get_quarter_roman(dt))
