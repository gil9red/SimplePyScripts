#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

from bs4 import BeautifulSoup

from common import ROOT_DIR

sys.path.append(str(ROOT_DIR))
from root_common import session


URL_FORMAT = (
    "https://helpdesk.compassluxe.com/issues/?jql=project %3D {project} "
    "AND resolution %3D Unresolved "
    "ORDER BY created DESC"
)


def get_last_issue_key(project: str) -> str:
    url = URL_FORMAT.format(project=project)

    rs = session.get(url)

    root = BeautifulSoup(rs.content, "html.parser")
    issue_row_el = root.select_one("tr[data-issuekey]")
    return issue_row_el["data-issuekey"]


if __name__ == "__main__":
    print(get_last_issue_key(project="OPTT"))
    print(get_last_issue_key(project="RADIX"))
    print(get_last_issue_key(project="TXPG"))
