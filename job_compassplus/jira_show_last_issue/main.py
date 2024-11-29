#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent
sys.path.append(str(ROOT_DIR))
from root_config import JIRA_HOST
from root_common import session


URL_SEARCH = f"{JIRA_HOST}/rest/api/latest/search"


def get_last_issue_key(project: str) -> str | None:
    query = {
        "jql": f"project={project} ORDER BY created DESC",
        "fields": "key",
        "maxResults": 1,
    }

    rs = session.get(URL_SEARCH, params=query)
    if rs.status_code == 400:
        return

    rs.raise_for_status()

    try:
        return rs.json()["issues"][0]["key"]
    except Exception:
        return


if __name__ == "__main__":
    import time

    for project in [
        "OPTT",
        "NOT_FOUND",
        "RADIX",
        "TXI",
        "TXACQ",
        "TXCORE",
        "TXISS",
        "TXPG",
        "TWO",
        "FLORA",
    ]:
        last_issue_key: str | None = get_last_issue_key(project=project)
        print(f"{project}: {last_issue_key if last_issue_key else '-'}", )
        time.sleep(0.5)
