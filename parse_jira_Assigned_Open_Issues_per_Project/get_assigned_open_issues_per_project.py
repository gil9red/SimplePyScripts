#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import Dict

import requests
from bs4 import BeautifulSoup

from common import DIR, print_table

URL = 'https://jira.compassplus.ru/secure/ViewProfile.jspa?name=ipetrash'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
}

# NOTE: Get <PEM_FILE_NAME>: openssl pkcs12 -nodes -out ipetrash.pem -in ipetrash.p12
PEM_FILE_NAME = str(DIR / 'ipetrash.pem')


def get_assigned_open_issues_per_project() -> Dict[str, int]:
    rs = requests.get(URL, headers=HEADERS, cert=PEM_FILE_NAME)
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
