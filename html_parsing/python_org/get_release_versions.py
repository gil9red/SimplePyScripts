#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

from dataclasses import dataclass
from datetime import date, datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag


HOST: str = "https://www.python.org"
HOST_DOCS: str = "https://docs.python.org"
URL_DOWNLOAD: str = f"{HOST}/downloads/"


def _parse_date(date_str: str) -> date:
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


def _get_tag(parent_el: Tag, selector: str) -> Tag:
    el: Tag | None = parent_el.select_one(selector)
    if not el:
        raise Exception(f"Not found element by selector {selector!r}")
    return el


def _get_tag_text(parent_el: Tag, selector: str) -> str:
    return _get_tag(parent_el, selector).get_text(strip=True)


def _get_tag_attr(parent_el: Tag, selector: str, attr: str) -> str:
    return _get_tag(parent_el, selector)[attr]


def _parse_version_from_tag(parent_el: Tag, selector: str) -> str:
    version: str = _get_tag_text(parent_el, selector)
    m = re.search(r"\d+\.\d+\.\d+|\d+\.\d+", version)
    if not m:
        raise Exception(f"Error in determining the version in {version!r}")

    return m.group()


def _parse_date_from_tag(parent_el: Tag, selector: str) -> date:
    date_str: str = _get_tag_text(parent_el, selector)
    return _parse_date(date_str)


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
        version: str = _parse_version_from_tag(el, ".release-version")

        return cls(
            version=version,
            status=_get_tag_text(el, ".release-status"),
            release_start=_parse_date_from_tag(el, ".release-start"),
            release_end=_parse_date_from_tag(el, ".release-end"),
            url_download=urljoin(
                HOST, _get_tag_attr(el, ".release-dl a[href]", "href")
            ),
            url_whatsnew=urljoin(HOST_DOCS, f"{version}/whatsnew/{version}.html"),
            url_release_pep=urljoin(
                HOST, _get_tag_attr(el, ".release-pep a[href]", "href")
            ),
        )


# TODO: Тесты
@dataclass
class ReleaseSpecificVersion:
    version: str
    release_date: date
    url_download: str
    url_changelog: str

    @classmethod
    def parse_from_soup(cls, el: Tag) -> "ReleaseSpecificVersion":
        version: str = _parse_version_from_tag(el, ".release-number")

        return cls(
            version=version,
            release_date=_parse_date_from_tag(el, ".release-date"),
            url_download=urljoin(
                HOST, _get_tag_attr(el, ".release-download a[href]", "href")
            ),
            url_changelog=urljoin(
                HOST_DOCS, _get_tag_attr(el, ".release-enhancements a[href]", "href")
            ),
        )


def get_release_versions() -> list[ReleaseVersion]:
    rs = requests.get(URL_DOWNLOAD)
    rs.raise_for_status()

    soup = BeautifulSoup(rs.content, "html.parser")
    return [
        ReleaseVersion.parse_from_soup(el)
        for el in soup.select(
            ".active-release-list-widget > ol.list-row-container > li"
        )
    ]


def get_release_specific_versions() -> list[ReleaseSpecificVersion]:
    rs = requests.get(URL_DOWNLOAD)
    rs.raise_for_status()

    soup = BeautifulSoup(rs.content, "html.parser")
    return [
        ReleaseSpecificVersion.parse_from_soup(el)
        for el in soup.select(".download-list-widget > ol.list-row-container > li")
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
        tc.assertEqual(_parse_date(date_str), expected)

    versions: list[ReleaseVersion] = get_release_versions()
    print(f"Versions ({len(versions)}): {', '.join(v.version for v in versions)}")
    print(f"Details ({len(versions)}):")
    for v in versions:
        print(f"    {v}")
    """
    Versions (7): 3.15, 3.14, 3.13, 3.12, 3.11, 3.10, 3.9
    Details (7):
        ReleaseVersion(version='3.15', status='pre-release', release_start=datetime.date(2026, 10, 1), release_end=datetime.date(2031, 10, 1), url_download='https://www.python.org/downloads/latest/python3.15/', url_whatsnew='https://docs.python.org/3.15/whatsnew/3.15.html', url_release_pep='https://peps.python.org/pep-0790/')
        ReleaseVersion(version='3.14', status='bugfix', release_start=datetime.date(2025, 10, 7), release_end=datetime.date(2030, 10, 1), url_download='https://www.python.org/downloads/latest/python3.14/', url_whatsnew='https://docs.python.org/3.14/whatsnew/3.14.html', url_release_pep='https://peps.python.org/pep-0745/')
        ReleaseVersion(version='3.13', status='bugfix', release_start=datetime.date(2024, 10, 7), release_end=datetime.date(2029, 10, 1), url_download='https://www.python.org/downloads/latest/python3.13/', url_whatsnew='https://docs.python.org/3.13/whatsnew/3.13.html', url_release_pep='https://peps.python.org/pep-0719/')
        ReleaseVersion(version='3.12', status='security', release_start=datetime.date(2023, 10, 2), release_end=datetime.date(2028, 10, 1), url_download='https://www.python.org/downloads/latest/python3.12/', url_whatsnew='https://docs.python.org/3.12/whatsnew/3.12.html', url_release_pep='https://peps.python.org/pep-0693/')
        ReleaseVersion(version='3.11', status='security', release_start=datetime.date(2022, 10, 24), release_end=datetime.date(2027, 10, 1), url_download='https://www.python.org/downloads/latest/python3.11/', url_whatsnew='https://docs.python.org/3.11/whatsnew/3.11.html', url_release_pep='https://peps.python.org/pep-0664/')
        ReleaseVersion(version='3.10', status='security', release_start=datetime.date(2021, 10, 4), release_end=datetime.date(2026, 10, 1), url_download='https://www.python.org/downloads/latest/python3.10/', url_whatsnew='https://docs.python.org/3.10/whatsnew/3.10.html', url_release_pep='https://peps.python.org/pep-0619/')
        ReleaseVersion(version='3.9', status='end-of-life, last release was3.9.25', release_start=datetime.date(2020, 10, 5), release_end=datetime.date(2025, 10, 31), url_download='https://www.python.org/downloads/latest/python3.9/', url_whatsnew='https://docs.python.org/3.9/whatsnew/3.9.html', url_release_pep='https://peps.python.org/pep-0596/')
    """

    print("\n" + "-" * 100 + "\n")

    specific_versions: list[ReleaseSpecificVersion] = get_release_specific_versions()
    print(
        f"Specific versions ({len(specific_versions)}):",
        ", ".join(v.version for v in specific_versions[:5]),
        "...",
        ", ".join(v.version for v in specific_versions[-5:]),
    )
    print(f"Details ({len(specific_versions)}):")
    for v in specific_versions[:5]:
        print(f"    {v}")
    print("    ...")
    for v in specific_versions[-5:]:
        print(f"    {v}")
    """
    Specific versions (245): 3.14.2, 3.14.1, 3.14.0, 3.13.11, 3.13.10 ... 2.2.2, 2.2.1, 2.2.0, 2.1.3, 2.0.1
    Details (245):
        ReleaseSpecificVersion(version='3.14.2', release_date=datetime.date(2025, 12, 5), url_download='https://www.python.org/downloads/release/python-3142/', url_changelog='https://docs.python.org/release/3.14.2/whatsnew/changelog.html')
        ReleaseSpecificVersion(version='3.14.1', release_date=datetime.date(2025, 12, 2), url_download='https://www.python.org/downloads/release/python-3141/', url_changelog='https://docs.python.org/release/3.14.1/whatsnew/changelog.html')
        ReleaseSpecificVersion(version='3.14.0', release_date=datetime.date(2025, 10, 7), url_download='https://www.python.org/downloads/release/python-3140/', url_changelog='https://docs.python.org/3.14/whatsnew/3.14.html')
        ReleaseSpecificVersion(version='3.13.11', release_date=datetime.date(2025, 12, 5), url_download='https://www.python.org/downloads/release/python-31311/', url_changelog='https://docs.python.org/release/3.13.11/whatsnew/changelog.html')
        ReleaseSpecificVersion(version='3.13.10', release_date=datetime.date(2025, 12, 2), url_download='https://www.python.org/downloads/release/python-31310/', url_changelog='https://docs.python.org/release/3.13.10/whatsnew/changelog.html')
        ...
        ReleaseSpecificVersion(version='2.2.2', release_date=datetime.date(2002, 10, 14), url_download='https://www.python.org/downloads/release/python-222/', url_changelog='http://hg.python.org/cpython/raw-file/v2.2.2/Misc/NEWS')
        ReleaseSpecificVersion(version='2.2.1', release_date=datetime.date(2002, 4, 10), url_download='https://www.python.org/downloads/release/python-221/', url_changelog='http://hg.python.org/cpython/raw-file/v2.2.1/Misc/NEWS')
        ReleaseSpecificVersion(version='2.2.0', release_date=datetime.date(2001, 12, 21), url_download='https://www.python.org/downloads/release/python-220/', url_changelog='http://hg.python.org/cpython/raw-file/v2.2/Misc/NEWS')
        ReleaseSpecificVersion(version='2.1.3', release_date=datetime.date(2002, 4, 9), url_download='https://www.python.org/downloads/release/python-213/', url_changelog='http://hg.python.org/cpython/raw-file/v2.1.3/Misc/NEWS')
        ReleaseSpecificVersion(version='2.0.1', release_date=datetime.date(2001, 6, 22), url_download='https://www.python.org/downloads/release/python-201/', url_changelog='http://hg.python.org/cpython/raw-file/v2.0.1/Misc/NEWS')
    """
