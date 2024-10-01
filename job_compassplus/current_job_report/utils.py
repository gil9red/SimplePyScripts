#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import sys

from datetime import datetime
from pathlib import Path

from lxml import etree

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


HOST = "https://helpdesk.compassluxe.com"
URL = f"{HOST}/pa-reports/"


def clear_hours(hours: str) -> str:
    return re.sub(r"[^\d:-]", "", hours)


def get_text_children(el: etree._Element, idx: int) -> str:
    try:
        return el.getchildren()[idx].text.strip()
    except IndexError:
        return ""


def _send_data(data: dict) -> str:
    # В какой-то момент адрес временно поменялся, тогда предварительный GET поможет получить актуальный адрес
    rs = session.get(URL)
    if not rs.ok:
        raise NotFoundReport(f"HTTP status is {rs.status_code}")

    rs = session.post(rs.url, data=data)
    if not rs.ok:
        raise NotFoundReport(f"HTTP status is {rs.status_code}")

    return rs.text


def get_report_context(dep: str = "all", rep: str = "rep1", period: str | None = None) -> str:
    today = datetime.today()

    if not period:
        period = today.strftime("%Y-%m")

    data = {
        "dep": dep,
        "rep": rep,
        "period": period,
        "v": int(today.timestamp() * 1000),
        "type": "normal",
    }
    return _send_data(data)


def get_quarter_report_context() -> str:
    today = datetime.today()
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
    today = datetime.today()
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
    dt = datetime.now()
    print(dt, get_quarter_num(dt), get_quarter_roman(dt))
