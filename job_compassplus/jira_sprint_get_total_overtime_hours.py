#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import sys

from dataclasses import dataclass
from datetime import datetime

from root_common import session


JIRA_HOST = "https://helpdesk.compassluxe.com"
URL_SEARCH = f"{JIRA_HOST}/rest/api/latest/search"

FIELD_OVERTIME_HOURS = "customfield_13440"

QUERY = {
    "jql": (
        "assignee = currentUser()"
        " AND project = Sprint AND type = Sub-task"
        " AND created >= startOfYear() AND created <= endOfYear()"
        " ORDER BY created DESC"
    ),
    "fields": f"key,created,{FIELD_OVERTIME_HOURS}",
}


@dataclass
class Sprint:
    key: str
    created: datetime
    overtime_hours: int


default_handler = logging.StreamHandler(stream=sys.stdout)
default_handler.setFormatter(
    logging.Formatter(
        "[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s"
    )
)
logger = logging.getLogger("jira_sprint_get_total_overtime_hours")
logger.setLevel(logging.WARNING)
logger.addHandler(default_handler)


def get_sprints_with_overtime_hours() -> list[Sprint]:
    logger.debug(f"Load: {URL_SEARCH}")

    rs = session.get(URL_SEARCH, params=QUERY)
    logger.debug(f"Response: {rs}")
    rs.raise_for_status()

    items: list[Sprint] = []

    issues = rs.json()["issues"]
    logger.info(f"Total issues: {len(issues)}")

    for issue in issues:
        key = issue["key"]
        created_str = issue["fields"]["created"]

        overtime_hours = issue["fields"][FIELD_OVERTIME_HOURS]
        overtime_hours: int = int(overtime_hours) if overtime_hours else 0

        logger.info(f"Issue: {key}, created_str: {created_str}, overtime hours: {overtime_hours}")

        items.append(
            Sprint(
                key=key,
                created=datetime.strptime(created_str, "%Y-%m-%dT%H:%M:%S.%f%z"),
                overtime_hours=overtime_hours,
            )
        )

    return items


if __name__ == "__main__":
    # NOTE: Debug
    # logger.setLevel(logging.DEBUG)

    total_overtime_hours = 0
    sprints = get_sprints_with_overtime_hours()
    print(f"Sprints ({len(sprints)}):")
    for i, sprint in enumerate(sprints, 1):
        print(f"    {i}. {sprint}")
        total_overtime_hours += sprint.overtime_hours

    print()
    print(f"Total overtime hours: {total_overtime_hours}")
