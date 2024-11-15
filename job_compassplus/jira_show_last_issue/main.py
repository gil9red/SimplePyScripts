#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent
sys.path.append(str(ROOT_DIR))
from root_common import session


JIRA_HOST = "https://helpdesk.compassluxe.com"
URL_SEARCH = f"{JIRA_HOST}/rest/api/latest/search"


def get_last_issue_key(project: str) -> str:
    query = {
        "jql": f"project={project} ORDER BY created DESC",
        "fields": "key",
        "maxResults": 1,
    }

    rs = session.get(URL_SEARCH, params=query)
    rs.raise_for_status()

    return rs.json()["issues"][0]["key"]


if __name__ == "__main__":
    import time

    for project in [
        "OPTT",
        "RADIX",
        "TXI",
        "TXACQ",
        "TXCORE",
        "TXISS",
        "TXPG",
        "TWO",
        "FLORA",
    ]:
        print(get_last_issue_key(project=project))
        time.sleep(0.5)
