#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import subprocess
import xml.etree.ElementTree as ET

from collections import defaultdict
from datetime import date, timedelta


PATTERN_VERSION = re.compile(r"/dev/(.+?)/")
URL_DEFAULT_SVN_PATH = "svn+cplus://svn2.compassplus.ru/twrbs/trunk/dev"


def search(text: str, last_days: int = 30, url: str = URL_DEFAULT_SVN_PATH) -> list[str]:
    end_date = date.today()
    start_date = date.today() - timedelta(days=last_days)

    data: bytes = subprocess.check_output(
        [
            "svn",
            "log",
            "--verbose",
            "--xml",
            "--search",
            text,
            "--revision",
            f"{{{start_date}}}:{{{end_date}}}",
            url,
        ]
    )

    root = ET.fromstring(data)

    revision_by_versions: dict[int, set[str]] = defaultdict(set)
    for logentry_el in root.findall(".//logentry"):
        revision = int(logentry_el.attrib["revision"])
        for path_el in logentry_el.findall("./paths/path"):
            if m := PATTERN_VERSION.search(path_el.text):
                revision_by_versions[revision].add(m.group(1))

    versions = []
    for _, rev_versions in sorted(revision_by_versions.items(), key=lambda x: x[0]):
        for version in rev_versions:
            if version not in versions:
                versions.append(version)

    return versions


if __name__ == "__main__":
    versions: list[str] = search(text="TXI-8210")
    print(versions)
    # ['trunk', '3.2.36.10', '3.2.35.10']

    versions: list[str] = search(
        text="OPTT-441",
        last_days=365,
        url="svn+cplus://svn2.compassplus.ru/twrbs/csm/optt",
    )
    print(versions)
    # ['trunk', '2.1.12.1']
