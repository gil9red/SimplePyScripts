#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import Dict
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# For import ascii_table__simple_pretty__ljust.py
import sys
sys.path.append('..')

from ascii_table__simple_pretty__ljust import print_pretty_table


URL = 'https://jira.compassplus.ru/secure/ViewProfile.jspa?name=ipetrash'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
}

# NOTE. Get <PEM_FILE_NAME>: openssl pkcs12 -nodes -out key.pem -in file.p12
PEM_FILE_NAME = 'ipetrash.pem'
PEM_FILE_NAME = str(Path(__file__).resolve().parent / PEM_FILE_NAME)


def get_assigned_open_issues_per_project() -> Dict[str, int]:
    rs = requests.get(URL, headers=HEADERS, cert=PEM_FILE_NAME)
    root = BeautifulSoup(rs.content, 'html.parser')

    data = dict()

    for item in root.select('#assigned-and-open > .mod-content > .stat-list > li'):
        name = item.select_one('a[title]').get_text(strip=True)
        value = int(item.select_one('.stat').get_text(strip=True))

        data[name] = value

    return data


if __name__ == '__main__':
    assigned_open_issues_per_project = get_assigned_open_issues_per_project()
    # print(assigned_open_issues_per_project)
    # # {'xxx': 1, 'yyy': 2, 'zzz': 3}

    print('Total issues:', sum(assigned_open_issues_per_project.values()))

    print()

    data = [("PROJECT", 'Issues')] + list(assigned_open_issues_per_project.items())
    print_pretty_table(data)
    # PROJECT | Issues
    # --------+-------
    # xxx     | 1
    # yyy     | 2
    # zzz     | 3
