#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

from dataclasses import dataclass
from datetime import datetime, date, timezone
from pathlib import Path
from typing import Any

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))
from site_common import do_get, do_post


@dataclass
class Vacation:
    id: int
    subject: str
    subject_email: str
    start_date: date
    end_date: date
    deputy: str

    @classmethod
    def parse_from_dict(cls, data: dict[str, Any]) -> "Vacation":
        def utc2local(dt_utc: datetime) -> datetime:
            epoch = dt_utc.timestamp()
            dt_local = datetime.fromtimestamp(epoch).replace(tzinfo=None)

            offset = dt_local - dt_utc.replace(tzinfo=None)
            return (dt_utc + offset).replace(tzinfo=None)

        def parse_datetime(date_time_str: str) -> datetime:
            # NOTE: Разбор даты из UTC "2024-08-18T19:00:00Z" в локальную дату
            return utc2local(datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S%z"))

        return cls(
            id=data["Id"],
            subject=data["Subject"],
            subject_email=data["EmailEmployee"],
            start_date=parse_datetime(data["StartDate"]),
            end_date=parse_datetime(data["EndDate"]),
            deputy=data["Location"],
        )


def get_vacations() -> list[Vacation]:
    url = "https://portal.compassplus.com/_api/web/lists/GetByTitle('Employee%20Vacations')/items"
    rs = do_get(
        url,
        headers={
            # NOTE: С такими заголовками сервер вернет JSON, а не XML
            "Accept": "application/json;odata.metadata=minimal",
            "odata-version": "4.0",
        },
        params={
            "$select": "Id,EndDate,Subject,Location,StartDate,EmailEmployee",
            "$top": "5000",
            "$orderby": "Subject asc",
            "$filter": f"(EndDate ge '{datetime.now(timezone.utc).date()}T00:00:00')",
        },
    )
    return [Vacation.parse_from_dict(value) for value in rs.json()["value"]]


if __name__ == "__main__":
    vacations = get_vacations()
    print(f"Vacations ({len(vacations)}):")
    for i, vacation in enumerate(vacations, 1):
        print(f"    {i}. {vacation}")
