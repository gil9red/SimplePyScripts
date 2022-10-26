#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
from typing import Dict

from bs4 import BeautifulSoup

from common import ROOT_DIR, print_table

sys.path.append(str(ROOT_DIR))
from root_common import session


URL = 'https://helpdesk.compassluxe.com/secure/ViewProfile.jspa?name=ipetrash'


def get_assigned_open_issues_per_project() -> Dict[str, int]:
    rs = session.get(URL)
    root = BeautifulSoup(rs.content, 'html.parser')

    data = dict()
    for item in root.select('#assigned-and-open > .mod-content > .stat-list > li'):
        name = item.select_one('a[title]').get_text(strip=True)
        value = int(item.select_one('.stat').get_text(strip=True))

        data[name] = value

    return data


def get_and_prints() -> Dict[str, int]:
    assigned_open_issues_per_project = get_assigned_open_issues_per_project()
    # {'xxx': 1, 'yyy': 2, 'zzz': 3}

    print('Total issues:', sum(assigned_open_issues_per_project.values()))
    print()

    print_table(assigned_open_issues_per_project)
    # PROJECT | Issues
    # --------+-------
    # xxx     | 1
    # yyy     | 2
    # zzz     | 3

    return assigned_open_issues_per_project


if __name__ == '__main__':
    get_and_prints()
