#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import sys

from root_common import session


HOST = "https://helpdesk.compassluxe.com"
URL_SEARCH = f"{HOST}/rest/api/latest/search"

FIELD_OVERTIME_HOURS = "customfield_13440"

QUERY = {
    "jql": (
        "assignee = currentUser()"
        " AND project = Sprint AND type = Sub-task"
        " AND updatedDate >= startOfMonth() AND updatedDate <= endOfMonth()"  # NOTE: Current month
    ),
    "fields": f"key,{FIELD_OVERTIME_HOURS}",
}

default_handler = logging.StreamHandler(stream=sys.stdout)
default_handler.setFormatter(
    logging.Formatter(
        "[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s"
    )
)
logger = logging.getLogger("jira_sprint_get_total_overtime_hours")
logger.setLevel(logging.WARNING)
logger.addHandler(default_handler)


def get_total_overtime_hours() -> int:
    logger.debug(f"Load: {URL_SEARCH}")

    rs = session.get(URL_SEARCH, params=QUERY)
    logger.debug(f"Response: {rs}")
    rs.raise_for_status()

    total_overtime_hours: int = 0

    issues = rs.json()["issues"]
    logger.info(f"Total issues: {len(issues)}")

    for issue in issues:
        key = issue["key"]

        overtime_hours = issue["fields"][FIELD_OVERTIME_HOURS]
        overtime_hours: int = int(overtime_hours) if overtime_hours else 0

        logger.info(f"Issue: {key}, overtime hours: {overtime_hours}")
        total_overtime_hours += overtime_hours

    logger.info(f"Total overtime hours: {total_overtime_hours}")

    return total_overtime_hours


if __name__ == "__main__":
    # NOTE: Debug
    # logger.setLevel(logging.DEBUG)

    print("Total overtime hours:", get_total_overtime_hours())
