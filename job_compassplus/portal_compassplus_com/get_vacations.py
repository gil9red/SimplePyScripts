#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import re
import xml.etree.ElementTree as ET

from dataclasses import dataclass
from datetime import datetime, date
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))
from site_common import do_get, do_post


@dataclass
class Vacation:
    subject: str
    start_date: date
    end_date: date
    deputy: str | None


def parse_datetime(date_time_str: str) -> datetime:
    # NOTE: "2024-08-18T19:00:00Z" -> "2024-08-18 19:00:00+00:00"
    return datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S%z")


def parse_name(name: str | None) -> str | None:
    if not name:
        return

    m = re.search(r"[a-z]+ [a-z]\.", name, flags=re.IGNORECASE)
    if not m:
        raise Exception(f"Не удалось найти имя из {name!r}")

    return m.group()


def get_vacations() -> list[Vacation]:
    url = (
        f"https://portal.compassplus.com/_api/web/lists/GetByTitle('empvacation')/items?"
        f"$top=5000&$orderby=Subject asc&$filter=EndDate ge '{datetime.utcnow().date()}T00:00:00Z'"
    )
    rs = do_get(url)

    ns = {
        "": "http://www.w3.org/2005/Atom",
        "d": "http://schemas.microsoft.com/ado/2007/08/dataservices",
        "m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata",
    }

    items: list[Vacation] = []

    root = ET.fromstring(rs.content)
    for props_el in root.findall("./entry/content/m:properties", namespaces=ns):
        subject_el = props_el.find("./d:Subject", namespaces=ns)
        start_date_el = props_el.find("./d:StartDate", namespaces=ns)
        end_date_el = props_el.find("./d:EndDate", namespaces=ns)

        # TODO: Странное название для тега того, кто замещает
        location_el = props_el.find("./d:Location", namespaces=ns)

        items.append(
            Vacation(
                subject=parse_name(subject_el.text),
                start_date=parse_datetime(start_date_el.text).date(),
                end_date=parse_datetime(end_date_el.text).date(),
                deputy=parse_name(location_el.text),
            )
        )

    return items


if __name__ == "__main__":
    vacations = get_vacations()
    print(f"Vacations ({len(vacations)}):")
    for i, vacation in enumerate(vacations, 1):
        print(f"{i}. {vacation}")
