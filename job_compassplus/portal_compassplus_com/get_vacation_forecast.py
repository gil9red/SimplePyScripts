#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))
from site_common import do_get, do_post


def get_vacation_forecast() -> int:
    url = "https://helpdesk.compassluxe.com/pa-reports-new/vacation/VacationForecast"
    rs = do_get(url)
    data: dict[str, int] = rs.json()
    return data["id"]


if __name__ == "__main__":
    vacation_forecast: int = get_vacation_forecast()
    print(f"Vacations:", vacation_forecast)
