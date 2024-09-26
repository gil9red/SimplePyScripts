#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from root_common import session


HOST = "https://helpdesk.compassluxe.com"
URL_SEARCH = f"{HOST}/rest/api/latest/search"

FIELD_OVERTIME_HOURS = "customfield_13440"

query = {
    "jql": (
        "assignee = currentUser()"
        " AND project = Sprint AND type = Sub-task"
        " AND updatedDate >= startOfMonth() AND updatedDate <= endOfMonth()"
    ),
    "fields": f"key,{FIELD_OVERTIME_HOURS}",
}

rs = session.get(
    URL_SEARCH,
    params=query,
)
rs.raise_for_status()

for issue in rs.json()["issues"]:
    key = issue["key"]

    overtime_hours = issue["fields"][FIELD_OVERTIME_HOURS]
    overtime_hours: int = int(overtime_hours) if overtime_hours else 0

    print(key, overtime_hours)
