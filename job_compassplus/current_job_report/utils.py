#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import enum
import re
import sys

from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))
from root_config import JIRA_HOST as HOST
from root_common import session

sys.path.append(str(DIR.parent.parent))
from get_quarter import (
    get_quarter_num,
    get_quarter_roman,  # NOTE: оставить get_quarter_roman для main.py
)


@enum.unique
class PeriodTypeEnum(enum.IntEnum):
    MONTH = 0
    QUARTER = 1
    PERIOD = 2


@enum.unique
class ReportTypeEnum(enum.IntEnum):
    WORKLOG = 5  # Отчет по зафиксированным трудозатратам
    SUMMARY = 6  # Сводный отчет


class NotFoundReport(Exception):
    pass


URL: str = f"{HOST}/pa-reports-new/report/"


def clear_hours(hours: str) -> str:
    return re.sub(r"[^\d:-]", "", hours)


def _send_data(data: dict[str, str | int]) -> str:
    # В какой-то момент адрес временно поменялся, тогда предварительный GET поможет получить актуальный адрес
    rs = session.get(URL)
    if not rs.ok:
        raise NotFoundReport(f"HTTP status is {rs.status_code}")

    # Добавление полей, типа токенов, если явно не были заданы
    soup = BeautifulSoup(rs.content, "html.parser")
    for el in soup.select('input[name][value][type="hidden"]'):
        name: str = el["name"]
        if name not in data:
            data[name] = el["value"]

    rs = session.post(rs.url, data=data)
    if not rs.ok:
        raise NotFoundReport(f"HTTP status is {rs.status_code}")

    return rs.text


def get_report(report_type: ReportTypeEnum, period_type: PeriodTypeEnum) -> str:
    today = datetime.today()

    data = {
        "reporttype": report_type.value,
        "PeriodType": period_type.value,
        "Month": today.month,
        "Year": today.year,
        "QuarterNum": get_quarter_num(today) - 1,  # NOTE: I квартал в отчете это 0
        "FromMonth": 1,
        "ToMonth": 12,
    }

    match report_type:
        case PeriodTypeEnum.QUARTER:
            data["quarter"] = "quarter"
        case PeriodTypeEnum.PERIOD:
            data["total"] = "total"

    return _send_data(data)


if __name__ == "__main__":
    dt = datetime.now()
    print(dt, get_quarter_num(dt), get_quarter_roman(dt))
