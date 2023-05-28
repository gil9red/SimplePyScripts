#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup

# pip install requests_ntlm2
from requests_ntlm2 import HttpNtlmAuth

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))
from root_common import session

from config import USERNAME, PASSWORD


@dataclass
class Employee:
    full_name: str
    user_name: str
    position: str
    url: str


session.auth = HttpNtlmAuth(USERNAME, PASSWORD)

URL = "https://mysite.compassplus.com/Person.aspx?accountname={}"


def get_employees(boss_username: str) -> list[Employee]:
    url = URL.format(boss_username)
    rs = session.get(url)
    rs.raise_for_status()

    root = BeautifulSoup(rs.content, "html.parser")
    root_table = root.select_one("#ReportingHierarchy")

    items = []

    for td in root_table.select(".ms-orgname"):
        a = td.a
        url = a["href"]
        items.append(
            Employee(
                full_name=a.get_text(strip=True),
                # Example: "https://.../Person.aspx?accountname=CP%5Cipetrash" -> "ipetrash"
                user_name=url.split("%5C")[-1],
                url=url,
                position=td.select_one(".ms_metadata").get_text(strip=True),
            )
        )

    return items


if __name__ == "__main__":
    from base64 import b64decode
    boss_username = b64decode("Q1BcbnZheW5lcg==").decode("utf-8")

    employees = get_employees(boss_username)
    print(f"Employees ({len(employees)}):")
    for i, employee in enumerate(employees, 1):
        print(f"{i}. {employee}")
    """
    ...
    9. Employee(full_name='Ilya A. Petrash', user_name='ipetrash', position='Senior Software Engineer', url='https://mysite.compassplus.com:443/Person.aspx?accountname=CP%5Cipetrash')
    ...
    """
    print()

    usernames = sorted(x.user_name for x in employees)
    print(usernames)
    print(", ".join(usernames))
