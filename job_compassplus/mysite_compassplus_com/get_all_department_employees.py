#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
from bs4 import BeautifulSoup
from common import URL, do_get, get_text


@dataclass
class Employee:
    full_name: str
    user_name: str
    position: str
    url: str


def get_employees(boss_username: str) -> list[Employee]:
    url: str = URL.format(boss_username)
    print("Load", url)

    rs = do_get(url)

    root = BeautifulSoup(rs.content, "html.parser")
    root_table = root.select_one("#ReportingHierarchy")

    items = []

    for td in root_table.select(".ms-orgname"):
        a = td.a
        url = a["href"]
        items.append(
            Employee(
                full_name=get_text(a),
                # Example: "https://.../Person.aspx?accountname=CP%5Cipetrash" -> "ipetrash"
                user_name=url.split("%5C")[-1],
                url=url,
                position=get_text(td.select_one(".ms_metadata")),
            )
        )

    return items


if __name__ == "__main__":
    from base64 import b64decode

    for boss_username in [
        b64decode("Q1BcbnZheW5lcg==").decode("utf-8"),
        b64decode("Q1BcYXZvc3RyaWtvdg==").decode("utf-8"),
        b64decode("Q1BceXJlbWl6b3Y=").decode("utf-8"),
    ]:
        print(f"Boss: {boss_username!r}")

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

        print("\n" + "-" * 100 + "\n")
