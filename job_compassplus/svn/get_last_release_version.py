#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import subprocess
import xml.etree.ElementTree as ET

from datetime import date, timedelta


TEXT_RELEASE_VERSION = "Release version "
PATTERN_RELEASE_VERSION = re.compile(rf"{TEXT_RELEASE_VERSION}([\d.]+) ")

URL_DEFAULT_SVN_PATH = "svn+cplus://svn2.compassplus.ru/twrbs/trunk/dev"


def get_last_release_version(
    version: str,
    start_revision: str = "HEAD",
    last_days: int = 30,
    url_svn_path: str = URL_DEFAULT_SVN_PATH,
) -> str:
    url = f"{url_svn_path}/{version}"

    end_date = date.today() - timedelta(days=last_days)

    data: bytes = subprocess.check_output(
        [
            "svn",
            "log",
            "--xml",
            "--search",
            TEXT_RELEASE_VERSION,
            "--revision",
            # Если в паре значений первым идет большее значение, то поиск будет идти от большего к меньшему
            f"{start_revision}:{{{end_date}}}",
            url,
        ]
    )
    root = ET.fromstring(data)

    last_release_version_msg = None
    for logentry_el in root.findall(".//logentry"):
        last_release_version_msg = logentry_el.find("msg").text
        break

    if not last_release_version_msg:
        raise Exception("Не удалось найти коммит релиза!")

    m = PATTERN_RELEASE_VERSION.search(last_release_version_msg)
    if not m:
        raise Exception(
            f"Не удалось вытащить версию релиза из {last_release_version_msg!r}"
        )

    return m.group(1)


if __name__ == "__main__":
    print(get_last_release_version(version="trunk", last_days=60))
    # 3.2.36.10

    print(get_last_release_version(version="3.2.35.10"))
    # 3.2.35.10.10

    print(get_last_release_version(version="3.2.34.10"))
    # 3.2.34.10.17
