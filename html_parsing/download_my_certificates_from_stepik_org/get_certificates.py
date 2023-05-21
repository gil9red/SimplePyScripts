#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests


def get_certificates(user: int) -> list[dict]:
    items = []

    s = requests.Session()
    page = 1
    while True:
        url = f"https://stepik.org/api/certificates?order=-id&page={page}&user={user}"

        rs = s.get(url)
        rs.raise_for_status()

        data = rs.json()
        items += data["certificates"]

        if not data["meta"]["has_next"]:
            break

        page += 1

    return items


if __name__ == "__main__":
    USER = 1381287  # https://stepik.org/users/1381287/certificates

    certificates = get_certificates(USER)
    print(f"Certificates ({len(certificates)}):")

    for cert in certificates:
        url = "https://stepik.org/course/" + str(cert["course"])
        print("   ", cert["course_title"], url)
        print("   ", cert["issue_date"])
        print("   ", cert["url"])
        print("   ", cert["preview_url"])
        print()
