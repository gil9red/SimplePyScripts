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


def search(
    text: str,
    last_days: int = 30,
    url_svn_path: str = URL_DEFAULT_SVN_PATH,
) -> list[str]:
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
            # Порядок имеет значение - выдача ревизий тут будет от меньшей к большей
            f"{{{start_date}}}:HEAD",
            url_svn_path,
        ]
    )

    root = ET.fromstring(data)

    versions = []
    for logentry_el in root.findall(".//logentry"):
        for path_el in logentry_el.findall("./paths/path"):
            if m := PATTERN_VERSION.search(path_el.text):
                version = m.group(1)
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
        url_svn_path="svn+cplus://svn2.compassplus.ru/twrbs/csm/optt",
    )
    print(versions)
    # ['trunk', '2.1.12.1']
