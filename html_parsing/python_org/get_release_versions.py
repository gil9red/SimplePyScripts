#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

from dataclasses import dataclass
from datetime import date, datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag


HOST: str = "https://www.python.org/"
HOST_DOCS: str = "https://docs.python.org/"


def parse_date(date_str: str) -> date:
    # EXAMPLES: "2026-10-01 (planned)", "2025-10-07", "2031-10", "Dec. 5, 2025", "June 3, 2025"

    if m := re.search(r"\d{4}-\d{2}-\d{2}", date_str):
        return datetime.strptime(m.group(), "%Y-%m-%d").date()
    elif m := re.search(r"\d{4}-\d{2}", date_str):
        return datetime.strptime(m.group(), "%Y-%m").date()
    elif m := re.search(
        r"(?P<month>[a-zA-Z]+)\.?\s+(?P<day>\d+).+?\s*(?P<year>\d{4})", date_str
    ):
        month_str: str = m["month"].lower()
        month_number: int = 0
        months: list[str] = [
            "jan",
            "feb",
            "mar",
            "apr",
            "may",
            "june",
            "july",
            "aug",
            "sep",
            "oct",
            "nov",
            "dec",
        ]
        for num, month_prefix in enumerate(months, start=1):
            if month_str.startswith(month_prefix):
                month_number = num
                break
        if not month_number:
            raise Exception(f"Error in determining the month in {date_str!r}")

        return date(
            year=int(m["year"]),
            month=month_number,
            day=int(m["day"]),
        )
    else:
        raise Exception(f"Unknown date format {date_str!r}")


def get_tag(parent_el: Tag, selector: str) -> Tag:
    el: Tag | None = parent_el.select_one(selector)
    if not el:
        raise Exception(f"Not found element by selector {selector!r}")
    return el


def get_tag_text(parent_el: Tag, selector: str) -> str:
    return get_tag(parent_el, selector).get_text(strip=True)


def get_tag_attr(parent_el: Tag, selector: str, attr: str) -> str:
    return get_tag(parent_el, selector)[attr]


@dataclass
class ReleaseVersion:
    version: str
    status: str
    release_start: date
    release_end: date
    url_download: str
    url_whatsnew: str
    url_release_pep: str

    @classmethod
    def parse_from_soup(cls, el: Tag) -> "ReleaseVersion":
        version: str = get_tag_text(el, ".release-version")

        return cls(
            version=version,
            status=get_tag_text(el, ".release-status"),
            release_start=parse_date(get_tag_text(el, ".release-start")),
            release_end=parse_date(get_tag_text(el, ".release-end")),
            url_download=urljoin(HOST, get_tag_attr(el, ".release-dl a[href]", "href")),
            url_whatsnew=urljoin(HOST_DOCS, f"{version}/whatsnew/{version}.html"),
            url_release_pep=urljoin(
                HOST, get_tag_attr(el, ".release-pep a[href]", "href")
            ),
        )


def get_release_versions() -> list[ReleaseVersion]:
    rs = requests.get(urljoin(HOST, "downloads/"))
    rs.raise_for_status()

    soup = BeautifulSoup(rs.content, "html.parser")
    return [
        ReleaseVersion.parse_from_soup(el)
        for el in soup.select(
            ".active-release-list-widget > ol.list-row-container > li"
        )
    ]


if __name__ == "__main__":
    # TODO: В tests/
    import unittest

    tc = unittest.TestCase()

    for date_str, expected in [
        ("2026-10-01 (planned)", date(2026, 10, 1)),
        ("2025-10-07", date(2025, 10, 7)),
        ("2031-10", date(2031, 10, 1)),
        ("Dec. 5, 2025", date(2025, 12, 5)),
        ("June 3, 2025", date(2025, 6, 3)),
    ]:
        tc.assertEqual(parse_date(date_str), expected)

    versions: list[ReleaseVersion] = get_release_versions()

    print(f"Versions ({len(versions)}): {', '.join(v.version for v in versions)}")
    # Versions (7): 3.15, 3.14, 3.13, 3.12, 3.11, 3.10, 3.9

    print(f"Details ({len(versions)}):")
    for v in versions:
        print(f"    {v}")
    """
    Details (7):
        ReleaseVersion(version='3.15', status='pre-release', release_start=datetime.date(2026, 10, 1), release_end=datetime.date(2031, 10, 1), url_download='https://www.python.org/downloads/latest/python3.15/', url_whatsnew='https://docs.python.org/3.15/whatsnew/3.15.html', url_release_pep='https://peps.python.org/pep-0790/')
        ReleaseVersion(version='3.14', status='bugfix', release_start=datetime.date(2025, 10, 7), release_end=datetime.date(2030, 10, 1), url_download='https://www.python.org/downloads/latest/python3.14/', url_whatsnew='https://docs.python.org/3.14/whatsnew/3.14.html', url_release_pep='https://peps.python.org/pep-0745/')
        ReleaseVersion(version='3.13', status='bugfix', release_start=datetime.date(2024, 10, 7), release_end=datetime.date(2029, 10, 1), url_download='https://www.python.org/downloads/latest/python3.13/', url_whatsnew='https://docs.python.org/3.13/whatsnew/3.13.html', url_release_pep='https://peps.python.org/pep-0719/')
        ReleaseVersion(version='3.12', status='security', release_start=datetime.date(2023, 10, 2), release_end=datetime.date(2028, 10, 1), url_download='https://www.python.org/downloads/latest/python3.12/', url_whatsnew='https://docs.python.org/3.12/whatsnew/3.12.html', url_release_pep='https://peps.python.org/pep-0693/')
        ReleaseVersion(version='3.11', status='security', release_start=datetime.date(2022, 10, 24), release_end=datetime.date(2027, 10, 1), url_download='https://www.python.org/downloads/latest/python3.11/', url_whatsnew='https://docs.python.org/3.11/whatsnew/3.11.html', url_release_pep='https://peps.python.org/pep-0664/')
        ReleaseVersion(version='3.10', status='security', release_start=datetime.date(2021, 10, 4), release_end=datetime.date(2026, 10, 1), url_download='https://www.python.org/downloads/latest/python3.10/', url_whatsnew='https://docs.python.org/3.10/whatsnew/3.10.html', url_release_pep='https://peps.python.org/pep-0619/')
        ReleaseVersion(version='3.9', status='end-of-life, last release was3.9.25', release_start=datetime.date(2020, 10, 5), release_end=datetime.date(2025, 10, 31), url_download='https://www.python.org/downloads/latest/python3.9/', url_whatsnew='https://docs.python.org/3.9/whatsnew/3.9.html', url_release_pep='https://peps.python.org/pep-0596/')
    """
