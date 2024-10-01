#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from pathlib import Path

from bs4 import BeautifulSoup

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent
sys.path.append(str(ROOT_DIR))
from root_common import session


URL_FORMAT: str = (
    "https://helpdesk.compassluxe.com/issues/"
    "?jql=project={project} ORDER BY created DESC"
)


def get_last_issue_key(project: str) -> str:
    url = URL_FORMAT.format(project=project)

    rs = session.get(url)
    rs.raise_for_status()

    root = BeautifulSoup(rs.content, "html.parser")
    issue_row_el = root.select_one("tr[data-issuekey]")
    return issue_row_el["data-issuekey"]


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
