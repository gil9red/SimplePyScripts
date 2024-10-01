#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import xml.etree.ElementTree as ET
import sys

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, date, timezone

from config import ROOT_DIR, USERNAME, MAX_RESULTS, JIRA_HOST

sys.path.append(str(ROOT_DIR))
from root_common import session

sys.path.append(str(ROOT_DIR.parent))
from logged_human_time_to_seconds import logged_human_time_to_seconds
from seconds_to_str import seconds_to_str


URL: str = (
    f"{JIRA_HOST}/activity?maxResults={MAX_RESULTS}"
    f"&streams=user+IS+{USERNAME}&os_authType=basic&title=undefined"
)


@dataclass
class Activity:
    entry_dt: datetime
    jira_id: str
    jira_title: str
    logged_human_time: str | None = None
    logged_seconds: int | None = None


# SOURCE: https://stackoverflow.com/a/13287083/5909792
def utc_to_local(utc_dt: datetime) -> datetime:
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def get_rss_jira_log() -> bytes:
    rs = session.get(URL)
    rs.raise_for_status()
    return rs.content


def get_date_by_activities(root) -> dict[date, list[Activity]]:
    ns = {
        "": "http://www.w3.org/2005/Atom",
        "activity": "http://activitystrea.ms/spec/1.0/",
    }

    def _get_text(el, xpath: str) -> str:
        return el.find(xpath, namespaces=ns).text.strip()

    result = defaultdict(list)

    pattern_logged = re.compile("logged '(.+?)'", flags=re.IGNORECASE)

    for entry in root.findall("./entry", namespaces=ns):
        # Ищем в <entry> строку с логированием
        if m := pattern_logged.search("".join(entry.itertext())):
            logged_human_time = m.group(1)
            logged_seconds = logged_human_time_to_seconds(logged_human_time)
        else:
            logged_human_time = logged_seconds = None

        try:
            jira_id = _get_text(entry, "./activity:object/title")
            jira_title = _get_text(entry, "./activity:object/summary")
        except:
            jira_id = _get_text(entry, "./activity:target/title")
            jira_title = _get_text(entry, "./activity:target/summary")

        # Переменная entry_dt имеет время в UTC, и желательно его привести в локальное время
        entry_dt = datetime.strptime(
            _get_text(entry, "./published"),
            "%Y-%m-%dT%H:%M:%S.%fZ",
        )
        entry_dt = utc_to_local(entry_dt)
        entry_date = entry_dt.date()

        result[entry_date].append(
            Activity(
                entry_dt=entry_dt,
                jira_id=jira_id,
                jira_title=jira_title,
                logged_human_time=logged_human_time,
                logged_seconds=logged_seconds,
            )
        )

    return result


def get_logged_dict(root) -> dict[str, list[dict]]:
    logged_dict = defaultdict(list)

    date_by_activities: dict[date, list[Activity]] = get_date_by_activities(root)
    for entry_date, activities in date_by_activities.items():
        date_str = entry_date.strftime("%d/%m/%Y")

        for activity in activities:
            if not activity.logged_human_time:
                continue

            logged_dict[date_str].append(
                {
                    "date_time": activity.entry_dt.strftime("%d/%m/%Y %H:%M:%S"),
                    "date": activity.entry_dt.strftime("%d/%m/%Y"),
                    "time": activity.entry_dt.strftime("%H:%M:%S"),
                    "logged_human_time": activity.logged_human_time,
                    "logged_seconds": activity.logged_seconds,
                    "jira_id": activity.jira_id,
                    "jira_title": activity.jira_title,
                }
            )

    return logged_dict


def parse_logged_dict(xml_data: bytes) -> dict[str, list[dict]]:
    root = ET.fromstring(xml_data)
    return get_logged_dict(root)


def get_sorted_logged(
    date_str_by_logged_list: dict, reverse=True
) -> list[tuple[str, list[dict]]]:
    sorted_items = date_str_by_logged_list.items()
    sorted_items = sorted(
        sorted_items, key=lambda x: datetime.strptime(x[0], "%d/%m/%Y"), reverse=reverse
    )

    return list(sorted_items)


def get_logged_list_by_now_utc_date(
    date_str_by_entry_logged_list: dict[str, list[dict]]
) -> list[dict]:
    current_utc_date_str = datetime.utcnow().strftime("%d/%m/%Y")
    return date_str_by_entry_logged_list.get(current_utc_date_str, [])


def get_logged_total_seconds(entry_logged_list: list[dict]) -> int:
    return sum(entry["logged_seconds"] for entry in entry_logged_list)


if __name__ == "__main__":
    print(URL)

    xml_data = get_rss_jira_log()
    print(len(xml_data), repr(xml_data[:50]))

    # open('rs.xml', 'wb').write(xml_data)
    # xml_data = open('rs.xml', 'rb').read()

    # Структура документа -- xml
    logged_dict = parse_logged_dict(xml_data)
    print(logged_dict)

    import json

    print(json.dumps(logged_dict, indent=4, ensure_ascii=False))
    print()

    logged_list = get_logged_list_by_now_utc_date(logged_dict)
    logged_total_seconds = get_logged_total_seconds(logged_list)
    print("entry_logged_list:", logged_list)
    print("today seconds:", logged_total_seconds)
    print("today time:", seconds_to_str(logged_total_seconds))
    print()

    # Для красоты выводим результат в табличном виде
    lines = []
    for date_str, logged_list in get_sorted_logged(logged_dict):
        total_seconds = get_logged_total_seconds(logged_list)
        lines.append((date_str, total_seconds, seconds_to_str(total_seconds)))

    # Список строк станет списком столбцов, у каждого столбца подсчитается максимальная длина
    max_len_columns = [max(map(len, map(str, col))) for col in zip(*lines)]

    # Создание строки форматирования: [30, 14, 5] -> "{:<30} | {:<14} | {:<5}"
    my_table_format = " | ".join("{:<%s}" % max_len for max_len in max_len_columns)

    for line in lines:
        print(my_table_format.format(*line))
